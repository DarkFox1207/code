package main

import "fmt"

func main() {

	var a int

	fmt.Print("Введите число: ")
	fmt.Scanln(&a) //Запрос на ввод данных от пользователя

	if a%2 == 0 { //Цикл Если и операция сравнения
		fmt.Println("Число четное")
	} else {
		fmt.Println("Число нечетное")
	}
}
