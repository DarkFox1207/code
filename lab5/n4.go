package main

import (
	"fmt"
	"math"
)

// Интерфейс Shape с методом Area
type Shape interface {
	Area() float64
}

// Структура Rectangle (прямоугольник)
type Rectangle struct {
	width, height float64
}

// Реализация метода Area() для Rectangle
func (r Rectangle) Area() float64 {
	return r.width * r.height
}

// Структура Circle (круг)
type Circle struct {
	radius float64
}

// Реализация метода Area() для Circle
func (c Circle) Area() float64 {
	return math.Pi * c.radius * c.radius
}

func main() {
	// Создание экземпляров Rectangle и Circle
	rect := Rectangle{width: 50, height: 50}
	circle := Circle{radius: 50}

	// Массив фигур, реализующих интерфейс Shape
	shapes := []Shape{rect, circle}

	// Вычисление и вывод площади для каждой фигуры
	for _, shape := range shapes {
		fmt.Printf("Площадь фигуры: %.2f\n", shape.Area())
	}
}
