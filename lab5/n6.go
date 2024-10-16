package main

import (
	"fmt"
)

// Интерфейс Stringer (из пакета fmt) требует реализации метода String()
type Stringer interface {
	String() string
}

// Структура Book для хранения информации о книге
type Book struct {
	title  string
	author string
	year   int
}

// Реализация метода String() для структуры Book
func (b Book) String() string {
	return fmt.Sprintf("Название книги: %s, Автор: %s, Год издания: %d", b.title, b.author, b.year)
}

func main() {
	// Создание экземпляра структуры Book
	book := Book{
		title:  "Ведьмак. Последнее желание",
		author: "Анжей Сапковский",
		year:   1986,
	}

	// Вывод строкового представления книги
	fmt.Println(book)
}
