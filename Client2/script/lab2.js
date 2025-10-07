// Ввод двух натуральных чисел
var n = parseInt(prompt("Введите первое число n:"));
var m = parseInt(prompt("Введите второе число m:"));

if (isNaN(n) || isNaN(m) || n <= 0 || m <= 0) {
    alert("Ошибка: введите два натуральных числа!");
} else {
    // Алгоритм Евклида с циклом
    var a = n, b = m;
    while (a !== b) {
        if (a > b) {
            a = a - b;
        } else {
            b = b - a;
        }
    }

    // Результат
    alert("НОД(" + n + ", " + m + ") = " + a);
}
