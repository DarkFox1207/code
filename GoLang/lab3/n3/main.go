package main

import (
	"bufio"                   //Пакет для работы с буферизованными вводом и выводом
	"fmt"                     //Пакет для форматированного ввода и вывода
	"os"                      //Пакет для работы с операционной системой, включая доступ к стандартному вводу
	"stringutils/stringutils" //Импортируем созданный пакет (папка/пакет)
)

func main() {
	//Сканер для чтения ввода с консоли
	scanner := bufio.NewScanner(os.Stdin)
	fmt.Print("Введите строку: ")
	// Чтение всей строки
	scanner.Scan()
	str := scanner.Text()
	// Переворачивание строки с помощью пакета stringutils
	rev := stringutils.Reverse(str)
	// Вывод перевернутой строки
	fmt.Println("Перевернутая строка:", rev)
}
