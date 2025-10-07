from fractions import Fraction

# Исходные точки
xs = [-4, -1, 0, 2]
ys = [25, -8, -15, -23]

def poly_mul(a, b):
    res = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            res[i + j] += ai * bj
    return res

# Построение многочлена Лагранжа
n = len(xs)
coeffs = [Fraction(0)] * n
for i in range(n):
    xi, yi = Fraction(xs[i]), Fraction(ys[i])
    num = [Fraction(1)]
    denom = Fraction(1)
    for j in range(n):
        if j != i:
            xj = Fraction(xs[j])
            num = poly_mul(num, [-xj, 1])  # (x - xj)
            denom *= (xi - xj)
    scale = yi / denom
    term = [c * scale for c in num]
    for k in range(len(term)):
        coeffs[k] += term[k]

# Форматирование многочлена
def poly_to_string(coeffs):
    terms = []
    for power, c in enumerate(coeffs):
        if c == 0:
            continue
        sign = "-" if c < 0 else "+"
        a = abs(c)
        if a == 1 and power != 0:
            coef_str = ""
        else:
            coef_str = str(a)
        if power == 0:
            term = f"{coef_str}"
        elif power == 1:
            term = f"{coef_str}*x" if coef_str else "x"
        else:
            term = f"{coef_str}*x^{power}" if coef_str else f"x^{power}"
        terms.append((sign, term))
    if not terms:
        return "0"
    s = ""
    for sign, term in reversed(terms):
        if s == "":
            s += term if sign == "+" else f"-{term}"
        else:
            s += f" {sign} {term}"
    return s

# Вывод многочлена
print("P(x) =", poly_to_string(coeffs))

# Вывод значений в заданных точках
for x in xs:
    val = sum(coeffs[k] * (x**k) for k in range(len(coeffs)))
    print(f"P({x}) = {val}")
