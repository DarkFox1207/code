import numpy as np

# Функция и её точные производные
def f(x):
    return (np.log2((2*x + 3)**2))**3

def f_prime_exact(x):
    return 3 * (np.log2((2*x+3)**2))**2 * (2 / ((2*x+3) * np.log(2)))

def f_double_prime_exact(x):
    ln2 = np.log(2)
    L = np.log2((2*x+3)**2)
    term1 = 6*L*(2/((2*x+3)*ln2))**2
    term2 = 3*L**2 * (-4/((2*x+3)**2 * ln2))
    return term1 + term2

# Функция для вычисления разностных производных
def compute_differences(x, y, h):
    n = len(x)
    dy_forward = np.zeros(n)
    dy_backward = np.zeros(n)
    dy_central = np.zeros(n)
    d2y = np.zeros(n)

    # Первая разностная производная
    dy_forward[:-1] = (y[1:] - y[:-1])/h 
    dy_forward[-1] = (y[-1] - y[-2])/h 

    dy_backward[1:] = (y[1:] - y[:-1])/h 
    dy_backward[0] = (y[1] - y[0])/h

    dy_central[1:-1] = (y[2:] - y[:-2])/(2*h) 
    dy_central[0] = (y[1] - y[0])/h
    dy_central[-1] = (y[-1] - y[-2])/h

    # Вторая разностная производная
    d2y[1:-1] = (y[2:] - 2*y[1:-1] + y[:-2])/h**2
    d2y[0] = (y[2] - 2*y[1] + y[0])/h**2
    d2y[-1] = (y[-1] - 2*y[-2] + y[-3])/h**2

    return dy_forward, dy_backward, dy_central, d2y

# Основная функция вывода таблицы
def print_table(h):
    x = np.arange(1, 8+h, h)
    y = f(x)
    dy_f, dy_b, dy_c, d2y = compute_differences(x, y, h)
    dy_exact = f_prime_exact(x)
    d2y_exact = f_double_prime_exact(x)
    
    print(f"\n{'='*80}")
    print(f"Результаты для h = {h}")
    print(f"{'x':>5} | {'dy_f':>10} | {'dy_b':>10} | {'dy_c':>10} | {'d2y':>10} | {'dy_ex':>10} | {'d2y_ex':>10} | {'Δdy_f':>8} | {'Δdy_b':>8} | {'Δdy_c':>8} | {'Δd2y':>8}")
    print('-'*80)
    
    for xi, df, db, dc, d2, dex, d2ex in zip(x, dy_f, dy_b, dy_c, d2y, dy_exact, d2y_exact):
        print(f"{xi:5.2f} | {df:10.4f} | {db:10.4f} | {dc:10.4f} | {d2:10.4f} | {dex:10.4f} | {d2ex:10.4f} | {abs(df-dex):8.4f} | {abs(db-dex):8.4f} | {abs(dc-dex):8.4f} | {abs(d2-d2ex):8.4f}")
    print(f"{'='*80}\n")

# Вывод таблиц для двух шагов
print_table(0.5)
print_table(0.1)

# dy_f Правая разностная производная
# dy_b Левая разностная производная
# dy_c Центральная разностная производная
# d2y Вторая разностная
# dy_ex Точное значение первой производной
# d2y_ex Точное значение первой производной
# Δdy_f Погрешность правая
# Δdy_b Погрешность левая
# Δdy_c Погрешность центральная
# Δd2y Погрешность второй разностной