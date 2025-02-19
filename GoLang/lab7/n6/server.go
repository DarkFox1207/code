package main

import (
	"fmt"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // Разрешаем соединения с любого источника (для разработки)
	},
}

type Client struct {
	conn *websocket.Conn
	send chan []byte
}

var (
	clients   = make(map[*Client]bool) // Подключенные клиенты
	broadcast = make(chan []byte)      // Канал для рассылки сообщений
	mu        sync.Mutex
)

func main() {
	http.HandleFunc("/ws", handleConnections)

	go handleMessages()

	fmt.Println("Сервер запущен на :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Println("Ошибка запуска сервера:", err)
	}
}

func handleConnections(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		fmt.Println("Ошибка при установке соединения:", err)
		return
	}
	client := &Client{conn: conn, send: make(chan []byte)}
	mu.Lock()
	clients[client] = true
	mu.Unlock()

	go handleMessagesForClient(client)

	for {
		_, msg, err := conn.ReadMessage()
		if err != nil {
			fmt.Println("Ошибка при чтении сообщения:", err)
			break
		}
		broadcast <- msg // Отправляем сообщение в канал рассылки
	}

	mu.Lock()
	delete(clients, client)
	mu.Unlock()
	conn.Close()
}

func handleMessagesForClient(client *Client) {
	for msg := range client.send {
		err := client.conn.WriteMessage(websocket.TextMessage, msg)
		if err != nil {
			fmt.Println("Ошибка при отправке сообщения:", err)
			break
		}
	}
}

func handleMessages() {
	for {
		msg := <-broadcast // Ожидание сообщений из канала рассылки
		mu.Lock()
		// Рассылаем сообщение всем подключенным клиентам
		for client := range clients {
			select {
			case client.send <- msg: // Отправляем сообщение клиенту
			default:
				close(client.send) // Закрываем канал, если клиент не может принять сообщение
				delete(clients, client)
			}
		}
		mu.Unlock()
	}
}
