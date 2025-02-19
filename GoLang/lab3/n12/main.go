package main

import (
	"fmt"
	"mathutils/mathutils" //Импортируем созданный пакет (папка/пакет)
)

func main() {
	n := 5
	fmt.Print("Факториал данного числа равен ", mathutils.Factorial(n))
}
