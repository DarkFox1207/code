package main

import "fmt"

func main() {

	var a, b int

	fmt.Print("Введите первое число: ")
	fmt.Scanln(&a) //Запрос на ввод данных от пользователя
	fmt.Print("Введите второе число: ")
	fmt.Scanln(&b)

	fmt.Println("Сумма =", a+b)
	fmt.Println("Разность a из b =", a-b)
	fmt.Println("Разность b из a=", b-a)
	fmt.Println("Умножение =", a*b)
	fmt.Println("Деление a на b =", a/b)
	fmt.Println("Деление b на a =", b/a)
	fmt.Println("Остаток от деления a на b =", a%b)
	fmt.Println("Остаток от деления b на a =", b%a)

}
