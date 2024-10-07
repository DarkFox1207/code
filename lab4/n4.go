package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Введите строку: ")
	input, _ := reader.ReadString('\n')
	// Убираем возможные лишние символы новой строки и пробелы
	input = strings.TrimSpace(input)
	// Преобразуем строку в верхний регистр
	upperInput := strings.ToUpper(input)
	fmt.Println("Строка в верхнем регистре:", upperInput)
}
