import numpy as np

# Данные
x = np.array([0.50, 0.75, 1.00, 1.25, 1.50])
y = np.array([1.732, 2.280, 3.000, 3.948, 5.196])

# 4 ближайших узла к x=1.30
x_nodes = x[1:]   # [0.75, 1.00, 1.25, 1.50]
y_nodes = y[1:]

# Строим кубический интерполяционный полином
coeffs = np.polyfit(x_nodes, y_nodes, 3)
P3 = np.poly1d(coeffs)

# Вычисляем значение в точке 1.30
x_val = 1.30
y_val = P3(x_val)

# Для оценки погрешности возьмём полином степени 4 (почти "истинное" значение)
true_poly = np.poly1d(np.polyfit(x, y, 4))
true_val = true_poly(x_val)
error = abs(true_val - y_val)

# Вывод
print("Коэффициенты P3(x):", coeffs)
print(f"P3(1.30) = {y_val:.6f}")
print(f"Оценка истинного значения ≈ {true_val:.6f}")
print(f"Погрешность ≈ {error:.6e}")
