#подключить инструмент для обработки командной строки

import argparse
import sys

from calc import equation
from calc import stats
from calc import series
from calc import integrate

from calc.arrays import MIN_VALUE, MAX_VALUE, MAX_COUNT
from calc.arrays import binary_search, generate_array
from calc.sorting import METHODS

def read_array(path=None):
#Читает массив целых чисел из файла или с клавиатуры
    if path:
        with open(path, encoding="utf-8-sig") as file:
            text = file.read()
    else:
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if not line.strip():
                break
            lines.append(line)
        text = " ".join(lines)
    text = text.replace(",", " ")
    words = text.split()
    numbers = []
    for word in words:
        numbers.append(int(word))
    if not 1 <= len(numbers) <= MAX_COUNT:
        raise ValueError("Количество элементов вне диапазона 1..1000000")
    for number in numbers:
        if not MIN_VALUE <= number <= MAX_VALUE:
            raise ValueError("Число вне диапазона -100..100")
    return numbers

def write_array(values, path):
    """Записывает массив целых чисел в файл"""
    text=" ".join(str(x) for x in values)+"\n"
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)

def fill_array(count, low, high, seed, output_path):
    #Создает случайный массив и записывает его в файл
    try:
        numbers=generate_array(count, low, high, seed)
        write_array(numbers, output_path)
    except(ValueError, OSError) as error:
        print(f"Ошибка:{error}", file=sys.stderr)
        return 1
    return 0

def sort_array(input_path, output_path, method, descending=False):
    #Читает массив, сортирует его и записывает результат
    try:
        numbers=read_array(input_path)
        sorting_function=METHODS[method]
        sorting_function(numbers, descending)
        write_array(numbers, output_path)
    except(ValueError, OSError, KeyError) as error:
            print(f"Ошибка:{error}", file=sys.stderr)
            return 1
    return 0

def search_array(input_path, target):
    #Ищет число в массиве и возвращает его значение
    try:
        numbers=read_array(input_path)
        index=binary_search(numbers, target)
        if index is not None:
            return numbers[index]
        return None
    except(ValueError, OSError) as error:
            print(f"Ошибка:{error}", file=sys.stderr)
            raise SystemExit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Программа для решения уравнений, обработки чисел, рядов и интегралов"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Команда solve
    solve_parser = subparsers.add_parser(
        "solve",
        help="Решение квадратного или линейного уравнения"
    )
    solve_parser.add_argument("-a", type=int, required=True)
    solve_parser.add_argument("-b", type=int, required=True)
    solve_parser.add_argument("-c", type=int, required=True)

    # Команда stats
    stats_parser = subparsers.add_parser("stats")
    stats_parser.add_argument("--input", type=str)

    # Команда series
    series_parser = subparsers.add_parser("series")
    series_parser.add_argument(
        "--func",
        choices=sorted(series.FORMULAS),
        required=True
    )

    group = series_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--terms", type=int)
    group.add_argument("--eps", type=float)

    # Команда integrate
    integrate_parser = subparsers.add_parser("integrate")
    integrate_parser.add_argument(
        "--func",
        choices=sorted(integrate.FORMULAS),
        required=True
    )
    integrate_parser.add_argument(
        "--from",
        dest="start",
        type=float,
        required=True
    )
    integrate_parser.add_argument(
        "--to",
        dest="end",
        type=float,
        required=True
    )
    integrate_parser.add_argument(
        "--steps",
        type=int,
        required=True
    )

    #Команда fill
    fill_parser = subparsers.add_parser("fill")
    fill_parser.add_argument("-c", "--count", type=int, required=True)
    fill_parser.add_argument("--min", dest="low", type=int, required=True)
    fill_parser.add_argument("--max", dest="high", type=int, required=True)
    fill_parser.add_argument("--seed", type=int)
    fill_parser.add_argument("-o", "--output", type=str, required=True)

    # Команда sort
    sort_parser = subparsers.add_parser("sort")
    sort_parser.add_argument("-i", "--input", type=str, required=True)
    sort_parser.add_argument("-o", "--output", type=str, required=True)
    sort_parser.add_argument("-m", "--method", choices=sorted(METHODS), required=True)
    sort_parser.add_argument("--descending", action="store_true")

    # Команда search
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("-i", "--input", type=str, required=True)
    search_parser.add_argument("-v", "--target", type=int, required=True)

    args = parser.parse_args()

    # Обработка команды fill
    if args.command == "fill":
        exit_code = fill_array(
            args.count,
            args.low,
            args.high,
            args.seed,
            args.output
            )
        raise SystemExit(exit_code)

    # Обработка команды sort
    elif args.command == "sort":
        exit_code = sort_array(
            args.input,
            args.output,
            args.method,
            args.descending
        )
        raise SystemExit(exit_code)
    
    # Oбработка команды search
    elif args.command == "search":
        result = search_array(args.input, args.target)
        if result is None:
            print("Число не найдено")
            raise SystemExit(1)
        print(result)

    # Обработка команды solve
    elif args.command == "solve":
        try:
            result = equation.solve_equation(args.a, args.b, args.c)

            print("Тип уравнения:", result["Тип уравнения"])

            if result["Дискриминант"] is not None:
                print("Дискриминант:", result["Дискриминант"])

            if len(result["Корни"]) == 0:
                print("Уравнение не имеет действительных корней")
            else:
                for i, root in enumerate(result["Корни"], start=1):
                    print(f"Корень x{i} = {root:.3f}")

        except ValueError as error:
            print("Ошибка:", error)

    # Обработка команды stats
    elif args.command == "stats":
        try:
            if args.input:
                with open(args.input, "r", encoding="utf-8") as source:
                    numbers = stats.read_numbers(source)
            else:
                numbers=[]
                while True:
                    line=input()
                    if line=='':
                        break
                    for i in line.split():
                        numbers.append(int(i))
                    
                # import sys
                # numbers = stats.read_numbers(sys.stdin)

            print_statistics = stats.calculate_all(numbers)

            for name, value, form in print_statistics:
                if isinstance(value, str):
                    print(f"{name}: НЕ СУЩЕСТВУЕТ")
                else:
                    print(f"{name}: {value:{form}}")

        except ValueError as error:
            print("Ошибка:", error)

    # Обработка команды series
    elif args.command == "series":
        try:
            term, formula = series.FORMULAS[args.func]

            print("Ряд:", args.func)
            print("Формула:", formula)

            if args.terms is not None:
                result = series.calculate_sum(term, args.terms)
            else:
                result, n = series.calculate_sum_eps(term, args.eps)

            print(f"Сумма: {result:.{series.DIGITS}f}")

        except ValueError as error:
            print("Ошибка:", error)
            raise SystemExit(1)

    # Обработка команды integrate
    elif args.command == "integrate":
        try:
            function, formula, low, high, strict = integrate.FORMULAS[args.func]

            integrate.check_limits(
                args.start,
                args.end,
                low,
                high,
                strict
            )

            result = integrate.calculate_integral(
                function,
                args.start,
                args.end,
                args.steps
            )

            print("Функция:", args.func)
            print("Формула:", formula)
            print(f"Интеграл: {result:.{integrate.DIGITS}f}")

        except ValueError as error:
            print("Ошибка:", error)
            raise SystemExit(1)


if __name__ == "__main__":
    main()