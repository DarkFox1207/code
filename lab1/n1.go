package main

import (
	"fmt"
	"time"
)

func main() {

	currentTime := time.Now() //Присвоить значение переменной текущее время
	fmt.Println("Текущее время: ", currentTime.String())

}
