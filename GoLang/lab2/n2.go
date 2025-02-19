package main

import "fmt"

func main() {

	var a float64

	fmt.Print("Введите число: ")
	fmt.Scanln(&a) //Запрос на ввод данных от пользователя

	//Вариант через if else if

	if a > 0 {
		fmt.Println("Positive")
	} else if a < 0 {
		fmt.Println("Negative")
	} else {
		fmt.Println("Zero")
	}

	//Вариант через switch case

	switch {
	case a > 0:
		fmt.Println("Positive")
	case a < 0:
		fmt.Println("Negative")
	default:
		fmt.Println("Zero")
	}

}
