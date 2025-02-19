// mathutils.go
package mathutils

// Factorial вычисляет факториал числа n.
func Factorial(n int) int {
	if n < 0 {
		return 0 // Для отрицательных чисел факториал не определен
	}
	if n == 0 || n == 1 {
		return 1
	}
	result := 1
	for i := 2; i <= n; i++ {
		result *= i
	}
	return result
}
