package main

import "fmt"

func main() {

	var a, b float64

	fmt.Print("Введите первое число: ")
	fmt.Scanln(&a) //Запрос на ввод данных от пользователя
	fmt.Print("Введите второе число: ")
	fmt.Scanln(&b)

	fmt.Println("Сумма =", a+b)
	fmt.Println("Разность a из b =", a-b)
	fmt.Println("Разность b из a=", b-a)

}
