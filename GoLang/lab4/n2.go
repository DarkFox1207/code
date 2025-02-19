package main

import "fmt"

// Функция для вычисления среднего возраста
func avgAge(people map[string]int) float64 {
	if len(people) == 0 {
		return 0 // если карта пуста, возвращаем 0
	}
	var totalAge int
	var count int

	for _, age := range people {
		totalAge += age
		count++
	}
	return float64(totalAge) / float64(count) // возвращаем средний возраст
}

func main() {
	// Пример карты с именами и возрастами людей
	people := map[string]int{
		"Алена":     250,
		"Борис":     30,
		"Владислав": 35,
		"Генадий":   20,
	}

	avg := avgAge(people)
	fmt.Printf("Средний возраст: %.1f\n", avg)
}
