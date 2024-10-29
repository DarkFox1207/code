package main

import (
	"bufio"
	"fmt"
	"net"
)

func main() {
	// Указываем порт, который будет прослушивать сервер
	port := "8080"
	// Запускаем сервер на указанном порту
	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		fmt.Println("Ошибка при запуске сервера:", err)
		return
	}
	defer listener.Close()
	fmt.Println("Сервер запущен на порту", port)

	for {
		// Ожидаем подключение клиента
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Ошибка при подключении клиента:", err)
			continue
		}
		fmt.Println("Подключен новый клиент")
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	// Считываем сообщение от клиента
	message, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		fmt.Println("Ошибка при чтении сообщения от клиента:", err)
		return
	}
	fmt.Println("Получено сообщение от клиента:", message)

	// Отправляем подтверждение клиенту
	confirmation := "Сообщение получено\n"
	_, err = conn.Write([]byte(confirmation))
	if err != nil {
		fmt.Println("Ошибка при отправке подтверждения:", err)
		return
	}
	fmt.Println("Подтверждение отправлено клиенту")
}
