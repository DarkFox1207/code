package main

import (
	"fmt"

	"mathutils/mathutils" // Импортируем созданный пакет (папка/пакет)
)

func main() {
	n := 5
	fmt.Printf("Factorial: \n", mathutils.Factorial(n))
}
