#Суммирование числовых рядов.

import math


MAX_TERMS = 10000
MAX_EPS = 0.0001
MAX_ITERATIONS = 100000

DIGITS = math.ceil(-math.log10(MAX_EPS))


def znak(n):
    if n % 2 == 0:
        return -1
    else:
        return 1


def term_sqplus(n):
    return znak(n) / (n * n + 1)


def term_third(n):
    return znak(n) / (3 * n)


FORMULAS = {
    "sqplus": (
        term_sqplus,
        "S = 1/(1^2+1) - 1/(2^2+1) + ..."
    ),
    "third": (
        term_third,
        "S = 1/3 - 1/6 + 1/9 - ..."
    )
}


def calculate_sum(term, count):
    if count < 1 or count > MAX_TERMS:
        raise ValueError("Количество слагаемых должно быть от 1 до 10000")

    result = 0

    for n in range(1, count + 1):
        result += term(n)

    return result


def calculate_sum_eps(term, eps):
    if not math.isfinite(eps) or eps <= 0 or eps > MAX_EPS:
        raise ValueError("Точность должна быть больше 0 и не превышать 0.0001")

    result = 0

    for n in range(1, MAX_ITERATIONS + 1):
        value = term(n)
        result += value

        if abs(value) < eps:
            return result, n

    raise ValueError("Заданная точность не достигнута")