import math
import numpy as np

def newton_method():
    print("\nМетод Ньютона")
    # Начальное приближение
    x, y = 0.5, -0.2
    
    # Параметры метода
    max_iter = 10
    tolerance = 1e-6
    step_limit = 1.0  # Максимальный шаг
    
    print(f"{'Итерация':<10} {'x':<15} {'y':<15} {'Норма Δ':<15}")
    print("-" * 60)
    
    for i in range(max_iter):
        # Вычисляем невязки
        f1 = math.sin(x + 0.5) - y - 1
        f2 = math.cos(y - 2) + x
        
        # Матрица Якоби
        J = np.array([
            [math.cos(x + 0.5), -1],
            [1, -math.sin(y - 2)]
        ])
        
        try:
            # Решаем систему
            delta = np.linalg.solve(J, [-f1, -f2])
            
            # Ограничиваем шаг
            norm = np.linalg.norm(delta)
            if norm > step_limit:
                delta = delta * step_limit / norm
                
            # Обновляем решение
            x += delta[0]
            y += delta[1]
            
            print(f"{i+1:<10} {x:<15.6f} {y:<15.6f} {norm:<15.6f}")
            
            # Проверка сходимости
            if norm < tolerance:
                print(f"\nМетод сошелся за {i+1} итераций")
                print(f"Решение: x = {x:.6f}, y = {y:.6f}")
                
                # Проверка невязки
                res1 = math.sin(x + 0.5) - y - 1
                res2 = math.cos(y - 2) + x
                return x, y
                
        except np.linalg.LinAlgError:
            print("Ошибка в вычислении матрицы Якоби")
            break
    
    print("Не достигнута сходимость")
    return x, y

newton_method()