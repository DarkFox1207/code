package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	// Адрес сервера и порт
	serverAddress := "localhost:8080"

	// Подключаемся к серверу
	conn, err := net.Dial("tcp", serverAddress)
	if err != nil {
		fmt.Println("Ошибка при подключении к серверу:", err)
		return
	}
	defer conn.Close()
	fmt.Println("Подключено к серверу", serverAddress)

	// Запрашиваем у пользователя ввод сообщения
	fmt.Print("Введите сообщение: ")
	message, err := bufio.NewReader(os.Stdin).ReadString('\n')
	if err != nil {
		fmt.Println("Ошибка при чтении сообщения:", err)
		return
	}

	// Отправляем сообщение серверу
	_, err = conn.Write([]byte(message))
	if err != nil {
		fmt.Println("Ошибка при отправке сообщения:", err)
		return
	}

	// Читаем ответ от сервера
	response, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		fmt.Println("Ошибка при получении ответа от сервера:", err)
		return
	}
	fmt.Println("Ответ от сервера:", response)
}
