import numpy as np
import matplotlib.pyplot as plt

# --- Данные ---
x = np.array([1.1, 1.7, 2.4, 3.0, 3.7, 4.5, 5.1, 5.8])
y = np.array([0.3, 0.6, 1.1, 1.7, 2.3, 3.0, 3.8, 4.6])

# --- Логарифмирование данных ---
ln_x = np.log(x)
ln_y = np.log(y)

# --- Линейная аппроксимация ln(y) = ln(c) + m * ln(x) ---
m, ln_c = np.polyfit(ln_x, ln_y, 1)
c = np.exp(ln_c)

print(f"Степенная аппроксимирующая функция: y = {c:.4f} * x^{m:.4f}")

# --- Вычисление аппроксимированных значений ---
x_smooth = np.linspace(min(x), max(x), 200)
y_fit = c * x_smooth**m

# --- График в обычных координатах ---
plt.figure(figsize=(8, 6))
plt.scatter(x, y, color='black', label='Экспериментальные данные', zorder=5)
plt.plot(x_smooth, y_fit, 'r-', label=f'Аппроксимация: y = {c:.4f}·x^{m:.4f}')
plt.title('Степенная аппроксимация функции')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# --- График в логарифмических координатах ---
plt.figure(figsize=(8, 6))
plt.scatter(ln_x, ln_y, color='blue', label='Логарифмированные данные', zorder=5)
plt.plot(ln_x, m*ln_x + ln_c, 'orange', label=f'Линейная аппроксимация ln(y) = {ln_c:.4f} + {m:.4f}·ln(x)')
plt.title('Линейная зависимость в логарифмических координатах')
plt.xlabel('ln(x)')
plt.ylabel('ln(y)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
