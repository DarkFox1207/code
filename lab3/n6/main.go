package main

import (
	"bufio" //Пакет для работы с буферизованными вводом и выводом
	"fmt"   //Пакет для форматированного ввода и вывода
	"os"    //Пакет для работы с операционной системой, включая доступ к стандартному вводу
)

func main() {
	//Считывать данные с консоли
	reader := bufio.NewReader(os.Stdin)
	//Запрос количества строк
	fmt.Print("Введите количество строк: ")
	var n int
	_, err := fmt.Scanf("%d\n", &n)
	//Обработчик ошибок ввода
	if err != nil || n <= 0 {
		fmt.Println("Ошибка: введите положительное целое число")
		return
	}

	//Создание среза для строк
	strings := make([]string, n)
	//Ввод строк от пользователя
	for i := 0; i < n; i++ {
		fmt.Printf("Введите строку %d: ", i+1)
		str, _ := reader.ReadString('\n')
		strings[i] = str[:len(str)-1] //Убираем символ новой строки
	}

	//Переменная для хранения самой длинной строки
	var longest string
	//Поиск самой длинной строки
	for _, str := range strings {
		if len(str) > len(longest) {
			longest = str
		}
	}
	// Вывод самой длинной строки
	fmt.Println("Самая длинная строка:", longest)
}
