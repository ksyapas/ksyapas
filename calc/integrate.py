#Численное интегрирование
import math

MAX_STEPS = 100000
DIGITS = 4

def F_ratio(x):
    return x / (x + 1)

def F_root(x):
    return (x * x + 1) ** 0.5

FORMULAS = {"ratio": (F_ratio,"F(x) = x / (x + 1)",0,20,False),"root": (F_root,"F(x) = sqrt(x^2 + 1)",-5,5,True)}

def calculate_integral(function, a, b, steps):
    if not math.isfinite(a) or not math.isfinite(b):
        raise ValueError("Пределы интегрирования должны быть конечными числами")
    if a >= b:
        raise ValueError("Нижний предел должен быть меньше верхнего")
    if not isinstance(steps, int) or steps < 1 or steps > MAX_STEPS:
        raise ValueError("Количество шагов должно быть от 1 до 100000")
    if steps < 1 or steps > MAX_STEPS:
        raise ValueError("Количество шагов должно быть от 1 до 100000")
    dx = (b - a) / steps
    result = 0
    for i in range(steps):
        x = a + i * dx
        result += function(x) * dx
    return result

def check_limits(a, b, low, high, strict):
    if strict:
        if a <= low or a >= high or b <= low or b >= high:
            raise ValueError("Пределы выходят за допустимый промежуток")
    else:
        if a < low or a > high or b < low or b > high:
            raise ValueError("Пределы выходят за допустимый промежуток")