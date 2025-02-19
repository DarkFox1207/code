package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// Функция для генерации случайных чисел
func generateRandomNumbers(count int, wg *sync.WaitGroup) {
	defer wg.Done()
	time.Sleep(1 * time.Second) // Имитация задержки
	fmt.Printf("Случайные числа: ")
	for i := 0; i < count; i++ {
		fmt.Printf("%d ", rand.Intn(100))
	}
	fmt.Println()
}

// Функция для расчёта факториала числа
func factorial(n int, wg *sync.WaitGroup) {
	defer wg.Done()             // Сообщаем, что горутина завершила выполнение
	time.Sleep(2 * time.Second) // Имитация задержки
	result := 1
	for i := 1; i <= n; i++ {
		result *= i
	}
	fmt.Printf("Факториал %d = %d\n", n, result)
}

// Функция для вычисления суммы числового ряда
func sumSeries(n int, wg *sync.WaitGroup) {
	defer wg.Done()
	time.Sleep(3 * time.Second) // Имитация задержки
	sum := 0
	for i := 1; i <= n; i++ {
		sum += i
	}
	fmt.Printf("Сумма ряда от 1 до %d = %d\n", n, sum)
}

func main() {
	var wg sync.WaitGroup // Используем WaitGroup для ожидания завершения всех горутин

	rand.Seed(time.Now().UnixNano()) // Инициализация генератора случайных чисел

	// Добавляем три горутины в группу ожидания
	wg.Add(3)
	// Запуск горутин
	go factorial(5, &wg)
	go generateRandomNumbers(5, &wg)
	go sumSeries(10, &wg)
	// Ожидаем завершения всех горутин
	wg.Wait()
	fmt.Println("Все горутины завершены.")
}
