#подключить инструмент для обработки командной строки

import argparse

from calc import equation
from calc import stats
from calc import series
from calc import integrate


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

    args = parser.parse_args()

    # Обработка команды solve
    if args.command == "solve":
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
                import sys
                numbers = stats.read_numbers(sys.stdin)

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