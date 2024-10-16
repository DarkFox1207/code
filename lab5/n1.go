package main

import "fmt"

// Структура Person
type Person struct {
	name string
	age  int
}

// Метод для вывода информации о человеке
func (p Person) PrintInfo() {
	fmt.Printf("Имя: %s, Возраст: %d\n", p.name, p.age)
}

func main() {
	// Создание экземпляра структуры Person
	person := Person{name: "Агафон", age: 18}

	// Вызов метода для вывода информации
	person.PrintInfo()
}
