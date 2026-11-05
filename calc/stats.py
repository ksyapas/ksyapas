#Статистика числового набора.

import math

def calculate_sum(numbers):
    result = 0
    for i in numbers:
        result+=i
    return result

def calculate_sred(numbers):
    result = 0
    for i in numbers:
        result+= i
    return result/len(numbers)

def calculate_sum_squares(numbers):
    result=0
    for i in numbers:
        result+=i**2
    return result

def calculate_root_sred_square(numbers):
    result=calculate_sum_squares(numbers)
    return (result/len(numbers))**0.5

def calculate_disper(numbers):
    sred=calculate_sred(numbers)
    summa=0
    for i in numbers:
        summa+=(i-sred)**2
    return summa/len(numbers)

def calculate_sko(numbers):
    return calculate_disper(numbers)**0.5

def calculate_standart(numbers):
    if len(numbers)<2:
        return 'Не существует'
    sred = calculate_sred(numbers)
    summa = 0
    for i in numbers:
        summa += (i - sred)**2
    return (summa / (len(numbers) - 1))**0.5

def calculate_min(numbers):
    return min(numbers)

def calculate_max(numbers):
    return max(numbers)

def calculate_polojit(numbers):
    kol=0
    for i in numbers:
        if i>0:
            kol+=1
    return kol

def calculate_otric(numbers):
    kol=0
    for i in numbers:
        if i<0:
            kol+=1
    return kol

SPISOK_POKAZAT=[
    ("Количество", len, "d"),
    ("Сумма", calculate_sum, ".3f"),
    ("Среднее арифметическое", calculate_sred, ".3f"),
    ("Сумма квадратов", calculate_sum_squares, ".3f"),
    ("Среднее квадратическое", calculate_root_sred_square, ".3f"),
    ("Дисперсия", calculate_disper, ".3f"),
    ("СКО", calculate_sko, ".3f"),
    ("Стандартное отклонение", calculate_standart, ".3f"),
    ("Наименьшее", calculate_min, ".3f"),
    ("Наибольшее", calculate_max, ".3f"),
    ("Положительных", calculate_polojit, "d"),
    ("Отрицательных", calculate_otric, "d")
]

def calculate_all(numbers):
    results = []
    for name, function, form in SPISOK_POKAZAT:
        value = function(numbers)
        results.append((name, value, form))
    return results

def print_statistics(numbers):
    results = calculate_all(numbers)
    for name, value in results:
        print(name + ":", value)

def read_numbers(source):
    numbers = []
    for line in source:
        for word in line.split():
            try:
                number = float(word)
                numbers.append(number)
            except ValueError:
                raise ValueError(f"{word} не является числом")
    if len(numbers) == 0:
        raise ValueError("Список чисел пуст")
    if len(numbers) > 20:
        raise ValueError("Нельзя вводить больше 20 чисел")
    for number in numbers:
        if not math.isfinite(number):
            raise ValueError("Число должно быть конечным")
    for number in numbers:
        if abs(number) > 10000:
            raise ValueError("Число не должно быть больше 10000 по модулю")
    return numbers