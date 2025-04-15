import math

def simple_iteration():
    print("Метод простых итераций")
    # Начальное приближение
    x, y = 0.5, -0.2
    
    # Параметры ускорения
    w = 0.92  # Оптимальный параметр релаксации
    history = []
    
    print(f"{'Итерация':<10} {'x':<15} {'y':<15} {'Δx':<15} {'Δy':<15}")
    print("-" * 60)
    
    for i in range(50):
        x_prev, y_prev = x, y
        
        # Итерационные формулы
        x = w * (-math.cos(y - 2)) + (1-w)*x
        y = w * (math.sin(x + 0.5) - 1) + (1-w)*y
        
        delta_x = abs(x - x_prev)
        delta_y = abs(y - y_prev)
        history.append((x, y, delta_x, delta_y))
        
        print(f"{i+1:<10} {x:<15.6f} {y:<15.6f} {delta_x:<15.6f} {delta_y:<15.6f}")
        
        if delta_x < 1e-6 and delta_y < 1e-6:
            print(f"\nСошлось за {i+1} итераций")
            print(f"Точное решение: x = {x:.6f}, y = {y:.6f}")
            return x, y
    
    print("Не сошлось")
    return x, y

simple_iteration()