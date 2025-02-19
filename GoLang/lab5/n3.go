package main

import (
	"fmt"
	"math"
)

// Структура Circle
type Circle struct {
	radius float64
}

// Метод для вычисления площади круга
func (c Circle) Area() float64 {
	return math.Pi * c.radius * c.radius
}

func main() {
	var radius float64

	// Ввод радиуса пользователем
	fmt.Print("Введите радиус круга: ")
	fmt.Scanln(&radius)

	// Создание экземпляра структуры Circle
	circle := Circle{radius: radius}

	// Вычисление и вывод площади круга
	fmt.Printf("Площадь данного круга: %.2f\n", circle.Area())
}
