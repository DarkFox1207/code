import numpy as np
from numpy.polynomial import Polynomial

# Данные
x = np.array([0.50, 0.75, 1.00, 1.25, 1.50])
y = np.array([1.732, 2.280, 3.000, 3.948, 5.196])

# Берем 4 ближайшие узла к x=0.65
x_nodes = x[:4]
y_nodes = y[:4]

# Строим интерполяционный многочлен 3-й степени (по Лагранжу)
coeffs = np.polyfit(x_nodes, y_nodes, 3)
P3 = np.poly1d(coeffs)

# Вычисляем значение в точке 0.65
x_val = 0.65
y_val = P3(x_val)

# Для оценки погрешности можно сравнить с полиномом 4-й степени (точнее аппроксимацией)
true_poly = np.poly1d(np.polyfit(x, y, 4))
true_val = true_poly(x_val)
error = abs(true_val - y_val)

# Вывод результатов
print("Коэффициенты P3(x):", coeffs)
print(f"P3(0.65) = {y_val:.6f}")
print(f"Оценка истинного значения ≈ {true_val:.6f}")
print(f"Погрешность ≈ {error:.6e}")
