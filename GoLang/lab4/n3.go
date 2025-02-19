package main

import "fmt"

// Функция для удаления записи по имени
func removePerson(people map[string]int, name string) {
	// Проверяем, существует ли запись с данным именем в карте
	if _, exists := people[name]; exists {
		delete(people, name) // Удаляем запись
		fmt.Printf("Запись с именем %s была удалена.\n", name)
	} else {
		fmt.Printf("Запись с именем %s не найдена.\n", name)
	}
}

func main() {
	// Пример карты с именами и возрастами людей
	people := map[string]int{
		"Алена":     25,
		"Борис":     30,
		"Владислав": 35,
		"Генадий":   20,
	}

	// Имя, которое нужно удалить
	var nameToRemove string
	fmt.Print("Введите имя для удаления: ")
	fmt.Scanln(&nameToRemove)
	removePerson(people, nameToRemove)

	// Выводим оставшиеся записи
	fmt.Println("Оставшиеся записи о людях:")
	for name, age := range people {
		fmt.Printf("Имя: %s, Возраст: %d\n", name, age)
	}
}
