package stringutils

//Возвращает строку в обратном порядке
func Reverse(s string) string {
	//Преобразуем строку в массив символов
	runes := []rune(s)
	for a, b := 0, len(runes)-1; a < b; a, b = a+1, b-1 {
		//Меняем местами символы
		runes[a], runes[b] = runes[b], runes[a]
	}
	//Преобразуем обратно в строку
	return string(runes)
}
