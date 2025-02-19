package main

import "fmt"

func main() {
	var n int
	fmt.Print("Введите количество элементов в массиве: ")
	fmt.Scan(&n)

	// Создаем срез для хранения чисел
	numbers := make([]int, n)

	// Считываем числа от пользователя
	for i := 0; i < n; i++ {
		fmt.Printf("Введите элемент %d: ", i+1)
		fmt.Scan(&numbers[i])
	}

	// Выводим массив в обратном порядке
	fmt.Println("Массив в обратном порядке:")
	for i := n - 1; i >= 0; i-- {
		fmt.Printf("%d ", numbers[i])
	}
	fmt.Println()
}
