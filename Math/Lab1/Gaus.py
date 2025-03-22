import numpy as np

def gauss_method(N, A, b):
    # Прямой ход метода Гаусса
    for i in range(N):
        # Проверяем на ноль диагональный элемент
        if A[i][i] == 0:
            raise ValueError("Нулевой элемент на диагонали, система не может быть решена методом Гаусса.")

        # Приведение главного элемента строки к единице
        for j in range(i + 1, N):
            factor = A[j][i] / A[i][i]
            A[j, i:] -= factor * A[i, i:]
            b[j] -= factor * b[i]

    # Обратный ход
    x = np.zeros(N, dtype=float)
    for i in range(N - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i][i]
    
    return x

def main():
    print("Решение СЛАУ методом Гаусса")
    print("-" * 40)

    N = 3
    # Исходная матрица и вектор свободных членов
    A = np.array([
        [3.19, 2.89, 2.47],
        [4.43, 4.02, 3.53],
        [3.40, 2.92, 2.40]
    ], dtype=float)
    
    b = np.array([33.91, 47.21, 32.92], dtype=float)

    print("Матрица коэффициентов A:")
    print(A)
    print("\nВектор свободных членов b:")
    print(b)

    try:
        x = gauss_method(N, A.copy(), b.copy())  # Передаем копии, чтобы сохранить исходные данные

        print("\nРешение системы:")
        for i in range(N):
            print(f"x{i + 1} = {x[i]:.6f}")

        print("\nПроверка решения:")
        for i in range(N):
            result = sum(A[i][j] * x[j] for j in range(N))
            print(f"Уравнение {i + 1}: {result:.6f} ≈ {b[i]}")

    except Exception as e:
        print(f"\nОшибка: {e}")

if __name__ == "__main__":
    main()
