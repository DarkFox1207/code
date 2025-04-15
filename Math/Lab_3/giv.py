import numpy as np

A = np.array([[1.03, 0.991],
              [0.991, 0.943]], dtype=np.float64)
b = np.array([2.51, 2.40], dtype=np.float64)

def improved_givens(A, b):
    # Создаем расширенную матрицу
    M = np.column_stack((A.copy(), b.copy()))
    
    # Шаг 1: Обнуляем элемент M[1,0]
    a, b_val = M[0,0], M[1,0]
    r = np.hypot(a, b_val)
    c = a/r
    s = b_val/r
    
    # Матрица вращения
    G = np.array([[c, s], [-s, c]], dtype=np.float64)
    
    # Применяем вращение
    M = G @ M
    
    # Шаг 2: Решаем треугольную систему
    x2 = M[1,2] / M[1,1]
    x1 = (M[0,2] - M[0,1]*x2) / M[0,0]
    
    # Итерационное уточнение
    for _ in range(3):
        r = b - A @ np.array([x1, x2])
        dx = np.linalg.solve(A.T @ A, A.T @ r)
        x1 += dx[0]
        x2 += dx[1]
    
    return np.array([x1, x2])

x_giv = improved_givens(A, b)

print("Метод Гивенса:")
print(f"Решение: x1 = {x_giv[0]:.6f}, x2 = {x_giv[1]:.6f}")