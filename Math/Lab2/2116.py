import numpy as np

def yakoby(A, b, n, max_iter=1000, tol=1e-6):
    
    x = np.zeros(n)  # Начальное приближение

    step = 0
    
    x_old = np.zeros(n)  # Старое приближение для проверки сходимости

    for step in range(max_iter):

        np.copyto(x_old, x)  # Копируем текущее значение x в x_old

        for i in range(n):
            # Вычисление нового значения для x[i]
            sum_ = b[i] - np.dot(A[i, :i], x[:i]) - np.dot(A[i, i+1:], x[i+1:])
            x[i] = sum_ / A[i, i]

        # Проверка на сходимость
        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            print(f"Система сходится за {step + 1} итераций")
            return x
    
    print(f"Максимальное количество итераций ({max_iter}) достигнуто")
    return x

# Обновленная система уравнений
A = np.array([
    [19.9000, 0.0849, 0.1020, 0.1191],
    [0.0626, 19.0000, 0.0969, 0.1140],
    [0.0576, 0.7470, 18.1000, 0.1090],
    [0.0525, 0.0696, 0.0867, 17.2000]
])

b = np.array([36.5001, 38.5997, 40.3345, 41.7045])

n = len(b)

x = yakoby(A, b, n)

print("Решение системы:", x)
