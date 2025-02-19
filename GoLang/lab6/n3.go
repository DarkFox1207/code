package main

import (
	"fmt"
	"math/rand"
	"time"
)

// Функция для генерации случайных чисел и отправки их в канал
func generateRandomNumbers(count int, ch chan int) {
	defer close(ch) // Закрываем канал после генерации всех чисел
	for i := 0; i < count; i++ {
		num := rand.Intn(100)              // Генерация случайного числа
		ch <- num                          // Отправляем число в канал
		time.Sleep(500 * time.Millisecond) // Имитация задержки
	}
}

// Функция для определения чётности/нечётности чисел
func checkEvenOdd(chNumbers chan int, chMessages chan string) {
	defer close(chMessages)      // Закрываем канал после завершения отправки сообщений
	for num := range chNumbers { // Чтение чисел из канала
		if num%2 == 0 {
			chMessages <- fmt.Sprintf("%d — чётное", num)
		} else {
			chMessages <- fmt.Sprintf("%d — нечётное", num)
		}
		time.Sleep(300 * time.Millisecond) // Имитация задержки
	}
}

func main() {
	rand.Seed(time.Now().UnixNano()) // Инициализация генератора случайных чисел

	// Создаем два канала: один для чисел, другой для сообщений
	chNumbers := make(chan int)
	chMessages := make(chan string)

	// Запуск горутины для генерации случайных чисел
	go generateRandomNumbers(10, chNumbers)

	// Запуск горутины для проверки чётности/нечётности чисел
	go checkEvenOdd(chNumbers, chMessages)

	// Используем select для приёма данных только из канала сообщений
	for msg := range chMessages {
		fmt.Println("Вывод:", msg)
	}

	fmt.Println("Все сообщения получены.")
}
