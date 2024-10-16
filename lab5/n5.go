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

// Функция, которая принимает срез интерфейсов Shape и выводит площадь каждого объекта
func PrintAreas(shapes []Shape) {
	for _, shape := range shapes {
		fmt.Printf("Area: %.2f\n", shape.Area())
	}
}

func main() {
	// Ввод данных для прямоугольника
	var width, height float64
	fmt.Print("Введите ширину прямоугольника: ")
	fmt.Scanln(&width)
	fmt.Print("Введите высоту прямоугольника: ")
	fmt.Scanln(&height)
	rect := Rectangle{width: width, height: height}

	// Ввод данных для круга
	var radius float64
	fmt.Print("Введите радиус круга: ")
	fmt.Scanln(&radius)
	circle := Circle{radius: radius}

	// Создание среза фигур
	shapes := []Shape{rect, circle}

	// Вызов функции для вывода площадей
	PrintAreas(shapes)
}
