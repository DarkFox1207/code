package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"github.com/jackc/pgx/v5/pgxpool"
)

// Структура пользователя с валидацией
type User struct {
	ID    int    `json:"id"`
	Fname string `json:"fname" validate:"required"`
	Sname string `json:"sname" validate:"required"`
	Age   int    `json:"age" validate:"gte=18"`
	Email string `json:"email" validate:"required,email"`
}

// Объявление глобальной переменной для подключения к базе данных
var db *pgxpool.Pool

func initDB() {
	dsn := "postgres://postgres:postgres@localhost:5432/userdb"
	var err error
	db, err = pgxpool.New(context.Background(), dsn)
	if err != nil {
		log.Fatalf("Не получилось подключится к БД: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("Подключено к БД")
}

// closeDB закрывает соединение с базой данных
func closeDB() {
	db.Close()
}

// Инициализация валидатора
var validate = validator.New()

// Функция валидации
func validateUser(user *User) error {
	return validate.Struct(user)
}

func main() {
	// Инициализация БД
	initDB()
	defer closeDB()

	// Инициализация Gin
	r := gin.Default()

	// Регистрация middleware
	r.Use(errorHandler)

	// Маршруты
	r.GET("/users", func(c *gin.Context) { getUsers(c, db) })
	r.GET("/users/:id", func(c *gin.Context) { getUserByID(c, db) })
	r.POST("/users", func(c *gin.Context) { createUser(c, db) })
	r.PUT("/users/:id", func(c *gin.Context) { updateUser(c, db) })
	r.DELETE("/users/:id", func(c *gin.Context) { deleteUser(c, db) })

	// Запуск сервера
	r.Run(":8080")
}

// errorHandler - middleware для централизованной обработки ошибок
func errorHandler(c *gin.Context) {
	c.Next()

	// Получаем ошибку, если она была
	if len(c.Errors) > 0 {
		// Возвращаем последнюю ошибку, если она есть
		c.JSON(http.StatusInternalServerError, gin.H{"error": c.Errors.Last().Error()})
	}
}

// GET /users - получение списка пользователей с пагинацией и фильтрацией
func getUsers(c *gin.Context, db *pgxpool.Pool) {
	page := c.DefaultQuery("page", "1")
	limit := c.DefaultQuery("limit", "10")
	fname := c.DefaultQuery("fname", "")
	age := c.DefaultQuery("age", "")

	// Преобразуем параметры в типы int
	pageInt, err := strconv.Atoi(page)
	if err != nil || pageInt < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Неправильный номер страницы"})
		return
	}

	limitInt, err := strconv.Atoi(limit)
	if err != nil || limitInt < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Неправильный лимит"})
		return
	}

	// Стартовый индекс для пагинации
	offset := (pageInt - 1) * limitInt

	// Построение запроса с динамической фильтрацией
	query := "SELECT id, fname, sname, age, email FROM users WHERE 1=1"
	args := []interface{}{}
	paramCounter := 1

	if fname != "" {
		query += fmt.Sprintf(" AND fname ILIKE $%d", paramCounter)
		args = append(args, "%"+fname+"%")
		paramCounter++
	}

	if age != "" {
		ageInt, err := strconv.Atoi(age)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Неправильный возраст"})
			return
		}
		query += fmt.Sprintf(" AND age = $%d", paramCounter)
		args = append(args, ageInt)
		paramCounter++
	}

	// Добавляем параметры пагинации в запрос
	query += fmt.Sprintf(" LIMIT $%d OFFSET $%d", paramCounter, paramCounter+1)
	args = append(args, limitInt, offset)

	// Выполнение запроса
	rows, err := db.Query(context.Background(), query, args...)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer rows.Close()

	users := []User{}
	for rows.Next() {
		var user User
		if err := rows.Scan(&user.ID, &user.Fname, &user.Sname, &user.Age, &user.Email); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		users = append(users, user)
	}

	// Возвращаем пользователей с пагинацией
	c.JSON(http.StatusOK, gin.H{
		"page":  pageInt,
		"limit": limitInt,
		"data":  users,
	})
}

// GET /users/:id - получение информации о конкретном пользователе
func getUserByID(c *gin.Context, db *pgxpool.Pool) {
	id := c.Param("id")
	var user User

	err := db.QueryRow(context.Background(), "SELECT id, fname, sname, age, email FROM users WHERE id=$1", id).
		Scan(&user.ID, &user.Fname, &user.Sname, &user.Age, &user.Email)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Пользователь не найден"})
		return
	}
	c.JSON(http.StatusOK, user)
}

// POST /users - добавление нового пользователя
func createUser(c *gin.Context, db *pgxpool.Pool) {
	var user User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Валидация
	if err := validateUser(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	err := db.QueryRow(context.Background(),
		"INSERT INTO users (fname, sname, age, email) VALUES ($1, $2, $3, $4) RETURNING id",
		user.Fname, user.Sname, user.Age, user.Email).Scan(&user.ID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusCreated, user)
}

// / PUT /users/:id - обновление информации о пользователе
func updateUser(c *gin.Context, db *pgxpool.Pool) {
	id := c.Param("id")
	var user User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Проверка, существует ли пользователь с таким ID
	var existingUser User
	err := db.QueryRow(context.Background(), "SELECT id FROM users WHERE id=$1", id).Scan(&existingUser.ID)
	if err != nil {
		// Если пользователь не найден, возвращаем ошибку
		if err == sql.ErrNoRows {
			c.JSON(http.StatusNotFound, gin.H{"error": "Пользователь не найден"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		}
		return
	}

	// Валидация
	if err := validateUser(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Обновление пользователя в базе данных
	_, err = db.Exec(context.Background(),
		"UPDATE users SET fname=$1, sname=$2, age=$3, email=$4 WHERE id=$5",
		user.Fname, user.Sname, user.Age, user.Email, id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Отправка ответа
	c.JSON(http.StatusOK, gin.H{"status": "Информация обновлена"})
}

// DELETE /users/:id - удаление пользователя
func deleteUser(c *gin.Context, db *pgxpool.Pool) {
	id := c.Param("id")

	// Проверка, существует ли пользователь
	var exists bool
	err := db.QueryRow(context.Background(), "SELECT EXISTS(SELECT 1 FROM users WHERE id=$1)", id).Scan(&exists)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Если пользователь не существует
	if !exists {
		c.JSON(http.StatusNotFound, gin.H{"error": "Пользователь не найден"})
		return
	}

	// Выполнение удаления
	_, err = db.Exec(context.Background(), "DELETE FROM users WHERE id=$1", id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Возвращаем успешный ответ
	c.JSON(http.StatusOK, gin.H{"status": "Пользователь удален"})
}
