import numpy as np

xr = 1.272
xs = np.array([1.22])
ys = np.array([11.9671])

# ----- Универсальная функция: разделённые разности -----
def divided_differences(xs, ys):
    n = len(xs)
    dd = np.zeros((n, n))
    dd[:,0] = ys
    for j in range(1, n):
        for i in range(n - j):
            dd[i,j] = (dd[i+1, j-1] - dd[i, j-1]) / (xs[i+j] - xs[i])
    coeffs = dd[0, :n]
    return coeffs, dd

def newton_eval(xs, coeffs, xr):
    # общая оценка по формуле Ньютона через коэффициенты разделённых разностей
    n = len(coeffs)
    result = 0.0
    prod = 1.0
    for k in range(n):
        result += coeffs[k] * prod
        prod *= (xr - xs[k])
    return result

coeffs, table = divided_differences(xs, ys)
Pxr = newton_eval(xs, coeffs, xr)

print("Узлы xs:", xs)
print("Значения ys:", ys)
print("Коэффициенты разделённых разностей:", coeffs)
print(f"P({xr}) = {Pxr:.6f}")
