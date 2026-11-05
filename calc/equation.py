#Вычисления для команды solve.
#файл equation.py должен отвечать за вычисления, 
# а вывод результата пользователю будет выполнять главный файл программы.
from sys import*
from math import*

kof=10000

def solve_equation(a, b, c):
    """Решает уравнение a*x^2 + b*x + c = 0."""

    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int):
        raise ValueError("Коэффициенты должны быть целыми числами")
    if abs(a)>kof or abs(b)>kof or abs(c)>kof:
        raise ValueError(f'Коэффициенты должны быть от {kof*-1} до {kof*1}')

    if a==0:
        if b==0:
            raise ValueError("A и B равны нулю")
        return {"Тип уравнения": "Линейное", "Корень":[-c/b], "Дискриминант":None}
    discriminant=b**2-4*a*c
    if discriminant<0:
        roots=[]
    elif discriminant==0:
        roots=[-b/(2*a)]
    else:
        roots=[(-b+sqrt(discriminant))/(2*a), (-b-sqrt(discriminant))/(2*a) ]
    return {"Тип уравнения": "Квадратное", "Корни": roots, "Дискриминант": discriminant}