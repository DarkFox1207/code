package main

import "fmt"

//Определение структуры Rectangle с 2 полями ширины и высоты
type Rectangle struct {
	Width  float64
	Height float64
}

//Функция Area принимает значение типа Rectangle (в данном случае это r) и возвращает площадь прямоугольника
func (r Rectangle) Area() float64 {
	return r.Width * r.Height
}

func main() {

	var w, h float64
	fmt.Print("Введите ширину прямоугольника: ")
	fmt.Scan(&w)
	fmt.Print("Введите высоту прямоугольника: ")
	fmt.Scan(&h)

	//Создание нового экземпляра структуры Rectangle
	r := Rectangle{Width: w, Height: h}

	//Вывод числа с 2 знаками после запятой
	fmt.Printf("Площадь прямоугольника: %.2f\n", r.Area())

}
