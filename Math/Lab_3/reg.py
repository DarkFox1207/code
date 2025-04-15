import numpy as np

# Исходные данные с повышенной точностью
A = np.array([[1.03, 0.991], 
              [0.991, 0.943]], dtype=np.float64)
b = np.array([2.51, 2.40], dtype=np.float64)

def solve_regularization(A, b, alpha):
    ATA = A.T @ A
    I = np.eye(2, dtype=np.float64)
    return np.linalg.solve(ATA + alpha*I, A.T @ b)

# Автоматический подбор alpha для совпадения с методом Гивенса
best_alpha = None
best_x = None
min_error = float('inf')

# Точный диапазон поиска (подбирается экспериментально)
for alpha in np.logspace(-6, -2, 1000):
    x = solve_regularization(A, b, alpha)
    # Проверяем невязку
    residual = np.linalg.norm(A @ x - b)
    if residual < 1e-6:  # Требуемая точность
        best_alpha = alpha
        best_x = x
        break

if best_alpha is None:
    # Если не нашли точного решения, берем наилучшее
    for alpha in np.logspace(-6, -2, 5000):
        x = solve_regularization(A, b, alpha)
        error = np.linalg.norm(A @ x - b)
        if error < min_error:
            min_error = error
            best_alpha = alpha
            best_x = x

print("Метод регуляризации:")
print(f"Оптимальный α = {best_alpha:.8f}")
print(f"Решение: x1 = {best_x[0]:.6f}, x2 = {best_x[1]:.6f}")