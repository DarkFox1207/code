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

// Метод для увеличения возраста на 1 год
func (p *Person) Birthday() {
	p.age++
}

func main() {
	// Создание экземпляра структуры Person
	person := Person{name: "Афродита", age: 23}

	// Вызов метода для вывода информации
	person.PrintInfo()

	// Увеличение возраста на 1 год
	person.Birthday()

	// Вывод информации после дня рождения
	person.PrintInfo()
}
