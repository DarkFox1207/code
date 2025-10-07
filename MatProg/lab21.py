import math

# Данные
x_values = [4, 9, 16, 25]
y_values = [math.sqrt(x) for x in x_values]

# Точка для вычисления
x_target = 11
y_true = math.sqrt(x_target)

# Линейная интерполяция между (9,3) и (16,4)
x0, y0 = 9, 3
x1, y1 = 16, 4

y_interp = y0 + (x_target - x0) * (y1 - y0) / (x1 - x0)

# Погрешности
abs_error = abs(y_true - y_interp)
rel_error = abs_error / y_true

print(f"Истинное значение: {y_true:.6f}")
print(f"Интерполяция: {y_interp:.6f}")
print(f"Абсолютная погрешность: {abs_error:.6f}")
print(f"Относительная погрешность: {rel_error:.6%}")
