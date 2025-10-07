import numpy as np

# Данные
x = np.array([1.7, 2.2, 2.4])
y = np.array([1.30, 1.48, 1.54])
x0 = 2.2  # точка, где ищем производные

# === 1. Метод Лагранжа ===
coeffs = np.polyfit(x, y, 2)  # аппроксимация многочленом второй степени
p = np.poly1d(coeffs)
p1 = np.polyder(p, 1)  # первая производная
p2 = np.polyder(p, 2)  # вторая производная

y1_lagr = p1(x0)
y2_lagr = p2(x0)

# === 2. Метод Ньютона ===
def divided_diff(x, y):
    n = len(x)
    coef = np.copy(y)
    for j in range(1, n):
        coef[j:n] = (coef[j:n] - coef[j - 1:n - 1]) / (x[j:n] - x[0:n - j])
    return coef

coef = divided_diff(x, y)

# Строим многочлен Ньютона и его производные вручную
def newton_poly_derivatives(x_data, coef, x0):
    n = len(coef)
    # первая производная
    dy = coef[1] + coef[2] * (2*x0 - x_data[0] - x_data[1])
    # вторая производная
    d2y = 2 * coef[2]
    return dy, d2y

y1_newt, y2_newt = newton_poly_derivatives(x, coef, x0)

# === Вывод результатов ===
print("=== Метод Лагранжа ===")
print(f"y'({x0}) = {y1_lagr:.6f}")
print(f"y''({x0}) = {y2_lagr:.6f}")

print("\n=== Метод Ньютона ===")
print(f"y'({x0}) = {y1_newt:.6f}")
print(f"y''({x0}) = {y2_newt:.6f}")
