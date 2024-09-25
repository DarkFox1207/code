package main

import (
	"fmt"

	"mathutils/mathutils" // Импортируем созданный пакет
)

func main() {
	n := 5
	fmt.Printf("Factorial: \n", mathutils.Factorial(n))
}
