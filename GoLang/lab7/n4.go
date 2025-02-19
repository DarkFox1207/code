package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

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

func main() {
	http.HandleFunc("/hello", helloHandler)
	http.HandleFunc("/data", dataHandler)

	// Запуск сервера на порту 8080
	fmt.Println("Starting server at :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
