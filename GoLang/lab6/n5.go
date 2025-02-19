package main

import (
	"fmt"
	"sync"
)

// Структура для хранения запроса на вычисление
type CalculationRequest struct {
	Operation string       // Операция (+, -, *, /)
	Num1      float64      // Первое число
	Num2      float64      // Второе число
	Result    chan float64 // Канал для отправки результата
}

// Сервер калькулятора: обрабатывает запросы на вычисление
func calculatorServer(requests chan CalculationRequest, wg *sync.WaitGroup) {
	defer wg.Done() // Сообщаем о завершении работы сервера

	for req := range requests {
		var result float64
		// Выполнение операции в зависимости от типа
		switch req.Operation {
		case "+":
			result = req.Num1 + req.Num2
		case "-":
			result = req.Num1 - req.Num2
		case "*":
			result = req.Num1 * req.Num2
		case "/":
			if req.Num2 != 0 {
				result = req.Num1 / req.Num2
			} else {
				fmt.Println("Ошибка: деление на ноль!")
				req.Result <- 0
				continue
			}
		default:
			fmt.Println("Ошибка: неподдерживаемая операция!")
			req.Result <- 0
			continue
		}
		// Отправка результата обратно через канал
		req.Result <- result
	}
}

// Клиентская горутина, отправляющая запросы на сервер
func client(id int, operation string, num1, num2 float64, requests chan CalculationRequest, wg *sync.WaitGroup) {
	defer wg.Done() // Сообщаем о завершении работы клиента

	// Создаём канал для получения результата
	resultChan := make(chan float64)

	// Отправляем запрос на сервер через канал
	requests <- CalculationRequest{
		Operation: operation,
		Num1:      num1,
		Num2:      num2,
		Result:    resultChan,
	}

	// Получаем результат из канала
	result := <-resultChan
	fmt.Printf("Клиент %d: %f %s %f = %f\n", id, num1, operation, num2, result)
}

func main() {
	var wgClients sync.WaitGroup
	var wgServer sync.WaitGroup

	// Создаём канал для запросов к калькулятору
	requests := make(chan CalculationRequest)

	// Запуск сервера калькулятора
	wgServer.Add(1)
	go calculatorServer(requests, &wgServer)

	// Запуск нескольких клиентских горутин
	operations := []struct {
		operation string
		num1      float64
		num2      float64
	}{
		{"+", 10, 5},
		{"-", 20, 5},
		{"*", 7, 6},
		{"/", 25, 5},
		{"/", 10, 0}, // Пример деления на ноль
		{"%", 15, 4}, // Пример неподдерживаемой операции
	}

	for i, op := range operations {
		wgClients.Add(1)
		go client(i+1, op.operation, op.num1, op.num2, requests, &wgClients)
	}

	// Ожидаем завершения всех клиентов
	wgClients.Wait()

	// Закрываем канал запросов, чтобы завершить работу сервера
	close(requests)

	// Ожидаем завершения работы сервера
	wgServer.Wait()

	fmt.Println("Калькулятор завершил обработку всех запросов.")
}
