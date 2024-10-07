package main

import "fmt"

func main() {
	// Создаем карту с именами людей и их возрастами
	people := map[string]int{
		"Алена":    20,
		"Борис":    25,
		"Владимир": 30,
	}

	// Добавляем нового человека
	people["Генадий"] = 35

	// Выводим все записи на экран
	fmt.Println("Записи о людях:")
	for name, age := range people {
		fmt.Printf("Имя: %s, Возраст: %d\n", name, age)
	}
}
