import numpy as np

def divided_differences(xs, ys):
    n = len(xs)
    # таблица n x n, заполненная нулями
    dd = np.zeros((n, n))
    dd[:,0] = ys
    for j in range(1, n):
        for i in range(n - j):
            dd[i,j] = (dd[i+1, j-1] - dd[i, j-1]) / (xs[i+j] - xs[i])
    # коэффициенты = первая строка (f[x0], f[x0,x1], f[x0,x1,x2], ...)
    return dd[0, :]

def newton_eval(xs, coeffs, xr):
    n = len(coeffs)
    result = 0.0
    mult = 1.0
    for k in range(n):
        result += coeffs[k] * mult
        mult *= (xr - xs[k])
    return result

xr = 1.275
xs = np.array([1.11])
ys = np.array([12.9122])

# Строим разделённые разности и оцениваем
coeffs = divided_differences(xs, ys)
P_xr = newton_eval(xs, coeffs, xr)

print("Узлы xs:", xs)
print("Значения ys:", ys)
print("Коэффициенты разделённых разностей (f[x0...xk]):", coeffs)
print(f"P({xr}) = {P_xr:.6f}")
