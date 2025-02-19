package main

import "fmt"

func main() {

	var a, b, c float64

	fmt.Print("Введите первое число: ")
	fmt.Scanln(&a) //Запрос на ввод данных от пользователя
	fmt.Print("Введите второе число: ")
	fmt.Scanln(&b)
	fmt.Print("Введите третье число: ")
	fmt.Scanln(&c)

	fmt.Println("Среднее значение =", (a+b+c)/3)

}
