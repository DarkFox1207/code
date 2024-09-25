package main

import (
	"fmt"
	"mathutils/mathutils" // Импортируем созданный пакет (папка/пакет)
)

func main() {
	var n int
	fmt.Print("Введите число: ")
	fmt.Scanln(&n)
	fmt.Print("Факториал данного числа равен ", mathutils.Factorial(n))
}
