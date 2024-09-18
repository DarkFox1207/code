package main

import "fmt"

func calc(a, b float64) (float64, float64, float64) {
	s1 := a + b
	s2 := a - b
	s3 := b - a
	return s1, s2, s3
}

func main() {
	var a, b float64
	fmt.Print("Введите первое число: ")
	fmt.Scan(&a)
	fmt.Print("Введите второе число: ")
	fmt.Scan(&b)

	//Вызов функции и присвоение значений от вычислений
	s1, s2, s3 := calc(a, b)
	fmt.Printf("Сумма = %.2f\n", s1)
	fmt.Printf("Разность a - b = %.2f\n", s2)
	fmt.Printf("Разность b - a = %.2f\n", s3)

}
