import numpy as np

def gauss_seidel_relaxation(A, b, w, tol=0.01, max_iterations=1000):
    
    n = len(b)  # Число переменных
    x = np.zeros(n)  # Начальное приближение
    iterations = 0  # Счетчик итераций
    
    print("Итерация\tРешение (x)\t\tРазница")
    while iterations < max_iterations:
        x_new = np.copy(x)  # Копируем текущее решение
        
        for i in range(n):
            # Вычисление суммы для первой и второй части строки
            sigma = sum(A[i][j] * x_new[j] for j in range(i)) + \
                    sum(A[i][j] * x[j] for j in range(i + 1, n))
            # Обновляем значение для x_i
            x_new[i] = (1 - w) * x[i] + (w / A[i][i]) * (b[i] - sigma)
    
        # Проверка на сходимость: если изменение вектора меньше порога, выходим
        diff = np.linalg.norm(x_new - x, ord=np.inf)
        print(f"{iterations}\t\t{np.round(x_new, 6)}\t\t{diff:.6f}")
        
        if diff < tol:
            break
        
        x = x_new  # Обновляем решение
        iterations += 1  # Увеличиваем количество итераций
    
    return x, iterations

# Обновленная система уравнений
A = np.array([
    [19.9000, 0.0849, 0.1020, 0.1191],
    [0.0626, 19.0000, 0.0969, 0.1140],
    [0.0576, 0.7470, 18.1000, 0.1090],
    [0.0525, 0.0696, 0.0867, 17.2000]
])

b = np.array([36.5001, 38.5997, 40.3345, 41.7045])

tolerance = 0.01  # Порог сходимости
max_iterations = 1000  # Максимальное количество итераций

w_values = [1.0, 1.8]  # Разные значения параметра омега

# Запуск метода с разными значениями w
for w in w_values:
    print(f"\nМетод релаксации с w = {w}:")
    solution, num_iterations = gauss_seidel_relaxation(A, b, w, tol=tolerance, max_iterations=max_iterations)
    print(f"Решение: {solution}")
    print(f"Количество итераций: {num_iterations}")
