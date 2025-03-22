import numpy as np

def khalezki_method(N, A, b):
    # Создаем нижнюю треугольную матрицу L
    L = np.zeros((N, N), dtype=complex)
    
    # Разложение Холецкого: A = L * L^T
    for i in range(N):
        for j in range(i+1):
            if i == j:
                # Диагональные элементы
                sum_k = sum(L[i][k] ** 2 for k in range(j))
                L[i][i] = np.sqrt(A[i][i] - sum_k)
            else:
                # Недиагональные элементы
                sum_k = sum(L[i][k] * L[j][k] for k in range(j))
                L[i][j] = (A[i][j] - sum_k) / L[j][j]
    
    # Решаем Ly = b (прямой ход)
    y = np.zeros(N, dtype=complex)
    for i in range(N):
        sum_k = sum(L[i][k] * y[k] for k in range(i))
        y[i] = (b[i] - sum_k) / L[i][i]
    
    # Решаем L^T * x = y (обратный ход)
    x = np.zeros(N, dtype=complex)
    for i in range(N-1, -1, -1):
        sum_k = sum(L[j][i] * x[j] for j in range(i+1, N))
        x[i] = (y[i] - sum_k) / L[i][i]
    
    return x

def main():
    print("Решение СЛАУ методом Холецкого с комплексными числами")
    print("-" * 40)
    
    N = 3
    # Новая исходная матрица для новой системы
    A_original = np.array([
        [3.19, 2.89, 2.47],
        [4.43, 4.02, 3.53],
        [3.40, 2.92, 2.40]
    ], dtype=complex)
    
    # Новый вектор свободных членов для новой системы
    b_original = np.array([33.91, 47.21, 32.92], dtype=complex)
    
    # Преобразование к системе A^T*A*x = A^T*b
    A = np.dot(A_original.T.conj(), A_original)  # Теперь матрица симметричная
    b = np.dot(A_original.T.conj(), b_original)
    
    print("Исходная матрица A:")
    print(A_original)
    print("\nПреобразованная матрица A^T*A:")
    print(A)
    print("\nПреобразованный вектор A^T*b:")
    print(b)
    
    try:
        x = khalezki_method(N, A, b)
        
        print("\nРешение системы:")
        for i in range(N):
            print(f"x{i+1} = {x[i]:.6f}")
        
        print("\nПроверка решения:")
        for i in range(N):
            result = sum(A_original[i][j] * x[j] for j in range(N))
            print(f"Уравнение {i+1}: {result:.6f} ≈ {b_original[i]}")
        
    except Exception as e:
        print(f"\nОшибка: {e}")

# Исправлена строка, чтобы проверка выполнялась корректно
if __name__ == "__main__":
    main()
