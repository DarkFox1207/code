package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"os/signal"
	"sync"
	"syscall"
)

var wg sync.WaitGroup              // Для ожидания завершения всех соединений
var shutdown = make(chan struct{}) // Канал для graceful shutdown

func main() {
	port := "8080"
	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		fmt.Println("Ошибка при запуске сервера:", err)
		return
	}
	defer listener.Close()
	fmt.Println("Сервер запущен на порту", port)

	// Канал для перехвата сигналов остановки
	sigint := make(chan os.Signal, 1)
	signal.Notify(sigint, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		<-sigint // Ожидаем сигнал
		fmt.Println("\nПолучен сигнал завершения, ожидаем завершения активных соединений...")
		close(shutdown) // Закрываем канал shutdown для уведомления горутин
		listener.Close()
	}()

	for {
		conn, err := listener.Accept()
		if err != nil {
			select {
			case <-shutdown: // Если сервер завершает работу, прерываем цикл
				fmt.Println("Сервер завершает работу")
				wg.Wait() // Ожидаем завершения всех горутин
				fmt.Println("Все соединения завершены. Сервер остановлен.")
				return
			default:
				fmt.Println("Ошибка при подключении клиента:", err)
				continue
			}
		}

		wg.Add(1)
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer wg.Done()
	defer conn.Close()

	select {
	case <-shutdown: // Завершаем, если сервер остановлен
		fmt.Println("Соединение закрыто, сервер завершает работу")
		return
	default:
	}

	message, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		fmt.Println("Ошибка при чтении сообщения от клиента:", err)
		return
	}
	fmt.Println("Получено сообщение от клиента:", message)

	confirmation := "Сообщение получено\n"
	_, err = conn.Write([]byte(confirmation))
	if err != nil {
		fmt.Println("Ошибка при отправке подтверждения:", err)
		return
	}
	fmt.Println("Подтверждение отправлено клиенту")
}
