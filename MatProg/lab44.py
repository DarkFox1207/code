import numpy as np
import matplotlib.pyplot as plt

# --- Исходные данные ---
x = np.array([-1.5, -1.3, -1.1, 1.2, 1.6, 1.8])
y = np.array([3.0, 2.8, 2.7, 2.1, 2.5, 3.1])

# --- Линейная аппроксимация (1-я степень) ---
coeffs1 = np.polyfit(x, y, 1)
y1_fit = np.polyval(coeffs1, x)
delta1 = np.sqrt(np.mean((y - y1_fit)**2))

# --- Квадратичная аппроксимация (2-я степень) ---
coeffs2 = np.polyfit(x, y, 2)
y2_fit = np.polyval(coeffs2, x)
delta2 = np.sqrt(np.mean((y - y2_fit)**2))

# --- Вывод результатов ---
print(f"Линейная аппроксимация: y = {coeffs1[0]:.4f}*x + {coeffs1[1]:.4f}")
print(f"Среднеквадратическое отклонение δ1 = {delta1:.4f}")
print(f"Квадратичная аппроксимация: y = {coeffs2[0]:.4f}*x^2 + {coeffs2[1]:.4f}*x + {coeffs2[2]:.4f}")
print(f"Среднеквадратическое отклонение δ2 = {delta2:.4f}")

# --- Построение графиков ---
x_smooth = np.linspace(min(x) - 0.5, max(x) + 0.5, 200)
y1_smooth = np.polyval(coeffs1, x_smooth)
y2_smooth = np.polyval(coeffs2, x_smooth)

plt.figure(figsize=(8, 6))
plt.scatter(x, y, color='black', label='Исходные точки', zorder=5)
plt.plot(x_smooth, y1_smooth, 'r--', label='Линейная аппроксимация')
plt.plot(x_smooth, y2_smooth, 'b-', label='Квадратичная аппроксимация')

plt.title("Аппроксимация экспериментальных данных")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
