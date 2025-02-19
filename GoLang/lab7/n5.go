package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
)

// Middleware для логирования запросов
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r) // Передаем управление следующему обработчику
		duration := time.Since(start)

		// Логируем метод, URL и время выполнения
		log.Printf("Method: %s, URL: %s, Duration: %v\n", r.Method, r.URL.Path, duration)
	})
}

// Обработчик для GET /hello
func helloHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Hello, welcome to our server!"))
	} else {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
	}
}

// Обработчик для POST /data
func dataHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodPost {
		var data map[string]interface{}

		// Парсим JSON из тела запроса
		err := json.NewDecoder(r.Body).Decode(&data)
		if err != nil {
			http.Error(w, "Bad Request", http.StatusBadRequest)
			return
		}

		// Выводим содержимое данных в консоль
		fmt.Println("Received data:", data)
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Data received successfully"))
	} else {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
	}
}

// Обработчик для GET /goodbye
func goodbyeHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Goodbye, see you next time!"))
	} else {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
	}
}

func main() {
	mux := http.NewServeMux() // Создаем новый маршрутизатор

	// Регистрация маршрутов
	mux.HandleFunc("/hello", helloHandler)
	mux.HandleFunc("/data", dataHandler)
	mux.HandleFunc("/goodbye", goodbyeHandler)

	// Обернуть маршрутизатор в middleware
	loggedMux := loggingMiddleware(mux)

	// Запуск сервера на порту 8080
	fmt.Println("Starting server at :8080")
	log.Fatal(http.ListenAndServe(":8080", loggedMux))
}
