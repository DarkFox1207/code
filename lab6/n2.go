package main

import (
	"fmt"
	"time"
)

// Функция для генерации чисел Фибоначчи и отправки их в канал
func generateFibonacci(n int, ch chan int) {
	defer close(ch) // Закрытие канала после завершения генерации
	a, b := 0, 1
	for i := 0; i < n; i++ {
		ch <- a // Отправляем число в канал
		a, b = b, a+b
		time.Sleep(500 * time.Millisecond) // Имитация задержки
	}
}

// Функция для чтения чисел из канала и их вывода
func printNumbers(ch chan int) {
	for num := range ch { // Чтение из канала до его закрытия
		fmt.Printf("Получено число: %d\n", num)
	}
}

func main() {
	ch := make(chan int) // Создаем канал для передачи чисел

	// Запускаем генерацию чисел Фибоначчи в отдельной горутине
	go generateFibonacci(10, ch)

	// Запускаем чтение чисел из канала в отдельной горутине
	printNumbers(ch)

	fmt.Println("Все числа Фибоначчи получены.")
}

//close(ch) закрывает канал, что предотвращает его дальнейшее использование для записи.
//Когда канал закрыт, горутина, которая считывает из него данные с помощью конструкции for num := range ch, завершит цикл чтения автоматически, как только все данные будут прочитаны.
//Без вызова close(), горутина чтения зависнет, ожидая новые данные, которых больше не будет.