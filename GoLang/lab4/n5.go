package main

import "fmt"

func main() {
	var n, sum int
	fmt.Print("Введите количество чисел, которые хотите суммировать:")
	fmt.Scan(&n)
	var num int
	// Цикл для считывания чисел и их суммирования
	for i := 0; i < n; i++ {
		fmt.Printf("Введите число %d: ", i+1)
		fmt.Scan(&num)
		sum += num
	}
	fmt.Printf("Сумма введенных чисел: %d\n", sum)
}
