package main

import (
	"fmt"

	"github.com/DarkFox1207/code/lab3/n1/mathutils" // Импортируем созданный пакет
)

func main() {
	n := 5
	fmt.Printf("Factorial: \n", mathutils.Factorial(n))
}
