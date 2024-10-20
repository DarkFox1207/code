package main

import (
	"bufio"
	"fmt"
	"os"
	"sync"
)

// Функция для реверсирования строки
func reverseString(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// Воркер, который обрабатывает задачи
func worker(id int, tasks <-chan string, results chan<- string, wg *sync.WaitGroup) {
	defer wg.Done()
	for task := range tasks {
		reversed := reverseString(task)
		fmt.Printf("Воркер %d обработал строку: %s -> %s\n", id, task, reversed)
		results <- reversed
	}
}

func main() {
	// Открытие файла для чтения строк
	file, err := os.Open("input.txt")
	if err != nil {
		fmt.Println("Ошибка открытия файла:", err)
		return
	}
	defer file.Close()

	// Чтение строк из файла
	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		fmt.Println("Ошибка чтения файла:", err)
		return
	}

	// Ввод количества воркеров от пользователя
	var numWorkers int
	fmt.Print("Введите количество воркеров: ")
	fmt.Scan(&numWorkers)

	// Создание каналов для задач и результатов
	tasks := make(chan string, len(lines))   // Буферизированный канал для задач
	results := make(chan string, len(lines)) // Буферизированный канал для результатов

	// Запуск воркеров
	var wg sync.WaitGroup
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go worker(i, tasks, results, &wg)
	}

	// Отправка задач воркерам
	for _, line := range lines {
		tasks <- line
	}

	// Закрываем канал задач, так как больше задач не будет
	close(tasks)

	// Ожидаем завершения всех воркеров
	wg.Wait()

	// Закрываем канал результатов
	close(results)

	// Открытие файла для записи результатов
	outputFile, err := os.Create("output.txt")
	if err != nil {
		fmt.Println("Ошибка создания файла:", err)
		return
	}
	defer outputFile.Close()

	// Запись результатов в файл
	for result := range results {
		_, err := outputFile.WriteString(result + "\n")
		if err != nil {
			fmt.Println("Ошибка записи в файл:", err)
			return
		}
	}

	fmt.Println("Все строки были обработаны и сохранены в файл output.txt")
}
