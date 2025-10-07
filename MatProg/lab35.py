import numpy as np
import matplotlib.pyplot as plt

# Таблица узлов
xs = np.array([-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
ys = np.array([-47, -38, -29, -20, -13, -11, -5, -2, 0, 0, 2, 3, 1, -2, -7, -10, -15, -24, -30, -37], dtype=float)

# Значение, в котором ищем f(x)
x_r = -4.2

# Функция для интерполяции по Лагранжу
def lagrange_interpolation(x, xs, ys):
    total = 0
    n = len(xs)
    for i in range(n):
        xi, yi = xs[i], ys[i]
        term = yi
        for j in range(n):
            if i != j:
                term *= (x - xs[j]) / (xi - xs[j])
        total += term
    return total

# Вычисляем приближённое значение
y_r = lagrange_interpolation(x_r, xs, ys)

print(f"Приближённое значение функции в точке x = {x_r}: y ≈ {y_r:.4f}")

# Построение интерполяционной кривой
x_vals = np.linspace(min(xs), max(xs), 500)
y_vals = [lagrange_interpolation(x, xs, ys) for x in x_vals]

plt.figure(figsize=(10,6))
plt.plot(xs, ys, 'ro', label='Исходные точки')
plt.plot(x_vals, y_vals, 'b-', label='Интерполяционная кривая (Лагранж)')
plt.axvline(x=x_r, color='green', linestyle='--', label=f'x = {x_r}')
plt.scatter([x_r], [y_r], color='purple', s=80, label=f'P({x_r}) = {y_r:.2f}')
plt.title("Интерполяция функции методом Лагранжа")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()
