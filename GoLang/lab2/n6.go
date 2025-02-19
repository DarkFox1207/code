package main

import "fmt"

//Функция вычисления среднего значения двух чисел вещественного типа
func average(a, b float64) float64 {
	return (a + b) / 2
}

func main() {

	var a, b float64
	fmt.Print("Введите первое число: ")
	fmt.Scan(&a)
	fmt.Print("Введите второе число: ")
	fmt.Scan(&b)
	avg := average(a, b)
	//Вывод с округлением до 2 знаков после запятой
	fmt.Printf("Среднее значение: %.2f\n", avg)

}
