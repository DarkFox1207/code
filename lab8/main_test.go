package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/stretchr/testify/assert"
)

// setupRouter создает роутер с нужными маршрутами для тестов
func setupRouter(db *pgxpool.Pool) *gin.Engine {
	r := gin.Default()
	r.GET("/users", func(c *gin.Context) { getUsers(c, db) })
	r.POST("/users", func(c *gin.Context) { createUser(c, db) })
	r.GET("/users/:id", func(c *gin.Context) { getUserByID(c, db) })
	r.PUT("/users/:id", func(c *gin.Context) { updateUser(c, db) })
	r.DELETE("/users/:id", func(c *gin.Context) { deleteUser(c, db) })
	return r
}

func TestGetUsers(t *testing.T) {
	initDB()
	defer closeDB()
	router := setupRouter(db)

	// Убедимся, что в базе есть хотя бы один пользователь
	// Задаем параметры запроса (можно изменять параметры фильтрации и пагинации для тестирования разных случаев)
	page := "1"
	limit := "10"
	fname := "Test" // Фильтрация по имени пользователя, если такой есть

	// Создаем GET-запрос с параметрами пагинации и фильтрации
	req, _ := http.NewRequest("GET", fmt.Sprintf("/users?page=%s&limit=%s&fname=%s", page, limit, fname), nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	// Проверка, что ответ имеет статус 200 OK
	assert.Equal(t, http.StatusOK, w.Code)

	// Проверка, что в ответе содержится правильная структура
	var response struct {
		Page  int    `json:"page"`
		Limit int    `json:"limit"`
		Data  []User `json:"data"`
	}
	err := json.Unmarshal(w.Body.Bytes(), &response)
	assert.NoError(t, err)

	// Проверка, что в данных есть пользователи
	assert.True(t, len(response.Data) > 0, "Не найдено пользователей в ответе")

	// Дополнительно можно проверить, что пагинация работает
	assert.Equal(t, 1, response.Page)
	assert.Equal(t, 10, response.Limit)
}

func TestGetUserByID(t *testing.T) {
	initDB()
	defer closeDB()
	router := setupRouter(db)

	// Задайте ID пользователя для получения. Измените значение testUserID по мере необходимости.
	testUserID := 1

	req, _ := http.NewRequest("GET", fmt.Sprintf("/users/%d", testUserID), nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
}

func TestCreateUser(t *testing.T) {
	initDB()
	defer closeDB()
	router := setupRouter(db)

	// Задайте данные для нового пользователя. Измените значения полей для тестирования других случаев.
	user := map[string]interface{}{
		"fname": "Test",                 // Имя
		"sname": "User",                 // Фамилия
		"age":   25,                     // Возраст
		"email": "testuser@example.com", // Email
	}
	userJSON, _ := json.Marshal(user)

	req, _ := http.NewRequest("POST", "/users", bytes.NewBuffer(userJSON))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusCreated, w.Code)

	// Проверка, что пользователь был создан
	var createdUser User
	err := json.Unmarshal(w.Body.Bytes(), &createdUser)
	assert.NoError(t, err)
	assert.NotEqual(t, 0, createdUser.ID)
}

func TestUpdateUser(t *testing.T) {
	initDB()
	defer closeDB()
	router := setupRouter(db)

	// ID пользователя, которого нужно обновить. Измените userID для тестирования других пользователей.
	userID := 20

	// Новые данные для пользователя. Измените поля, чтобы протестировать обновление.
	user := map[string]interface{}{
		"fname": "Updated",                 // Новое имя
		"sname": "User",                    // Новая фамилия
		"age":   30,                        // Новый возраст
		"email": "updateduser@example.com", // Новый email
	}
	userJSON, _ := json.Marshal(user)

	req, _ := http.NewRequest("PUT", fmt.Sprintf("/users/%d", userID), bytes.NewBuffer(userJSON))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
}

func TestDeleteUser(t *testing.T) {
	initDB()
	defer closeDB()
	router := setupRouter(db)

	// ID пользователя, которого нужно удалить. Измените userID для тестирования других пользователей.
	userID := 19

	req, _ := http.NewRequest("DELETE", fmt.Sprintf("/users/%d", userID), nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
}
