"""Измерение времени семи сортировок для лабораторной работы № 4.

Положите этот файл в корневую папку проекта рядом с laba_4.py,
затем запустите: python measure_time.py

Скрипт создаёт исходные массивы на 1000, 3000 и 10000 элементов
с seed=1, выполняет по три запуска каждого метода и сохраняет
таблицу в time_results.txt.
"""

from pathlib import Path
import re
import subprocess
import sys


PROJECT_DIR = Path(__file__).resolve().parent
PROGRAM = PROJECT_DIR / "laba_4.py"
SIZES = (1000, 3000, 10000)
METHODS = ("bubble", "selection", "insertion", "counting", "quick", "merge", "heap")
REPEATS = 3
RESULTS_DIR = PROJECT_DIR / "time_results"
REPORT_FILE = PROJECT_DIR / "time_results.txt"
TESTS_FILE = PROJECT_DIR / "tests.txt"
START_MARKER = "--- НАЧАЛО ЗАМЕРОВ ВРЕМЕНИ ЛР4 ---"
END_MARKER = "--- КОНЕЦ ЗАМЕРОВ ВРЕМЕНИ ЛР4 ---"

# Поддерживает оба варианта вывода времени:
# «Время сортировки quick: 0.000123 секунд»
# «Время операции sort (quick): 0.000123 с»
TIME_PATTERN = re.compile(
    r"время[^\r\n]*?([0-9]+(?:[.,][0-9]+)?)",
    re.IGNORECASE,
)


def run_command(command):
    """Выполняет команду проекта и возвращает её stdout и stderr."""
    result = subprocess.run(
        command,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        details = "\n".join(part for part in (result.stdout, result.stderr) if part.strip())
        raise RuntimeError(
            "Команда завершилась с ошибкой:\n"
            + " ".join(map(str, command))
            + ("\n" + details if details else "")
        )

    return result.stdout, result.stderr


def create_input_files():
    """Создаёт исходные файлы по требованиям лабораторной работы."""
    print("Создаю исходные массивы...")

    for count in SIZES:
        input_file = PROJECT_DIR / f"data_{count}.txt"
        command = [
            sys.executable,
            str(PROGRAM),
            "fill",
            "-c",
            str(count),
            "--seed",
            "1",
            "-o",
            str(input_file),
        ]
        run_command(command)
        print(f"  Создан {input_file.name}")


def get_elapsed_time(stdout, stderr, method):
    """Извлекает число секунд из сообщения, напечатанного параметром --time."""
    combined = stdout + "\n" + stderr
    for line in combined.splitlines():
        if "время" not in line.lower():
            continue
        match = TIME_PATTERN.search(line)
        if match:
            return float(match.group(1).replace(",", "."))

    raise RuntimeError(
        f"Не удалось найти время для метода {method}.\n"
        "Проверьте, что в cli.py добавлен параметр --time и при его использовании "
        "программа печатает строку с временем сортировки.\n"
        f"Вывод программы:\n{combined}"
    )


def measure_one(input_file, output_file, method):
    """Запускает один замер; программа заново читает исходный файл."""
    command = [
        sys.executable,
        str(PROGRAM),
        "sort",
        "-m",
        method,
        "-i",
        str(input_file),
        "-o",
        str(output_file),
        "--time",
    ]
    stdout, stderr = run_command(command)

    if not output_file.exists():
        raise RuntimeError(f"Не создан файл результата: {output_file}")

    return get_elapsed_time(stdout, stderr, method)


def make_report(rows):
    """Формирует таблицу из 21 строки с тремя замерами и средним временем."""
    lines = [
        "Лабораторная работа № 4. Сравнение времени сортировок",
        "Время указано в секундах. Для каждого метода выполнено три запуска.",
        "",
        f"{'Количество':<12} {'Метод':<12} {'t1':>12} {'t2':>12} {'t3':>12} {'Среднее':>12}",
        "-" * 76,
    ]

    for count, method, values in rows:
        average = sum(values) / len(values)
        lines.append(
            f"{count:<12} {method:<12} "
            f"{values[0]:>12.6f} {values[1]:>12.6f} "
            f"{values[2]:>12.6f} {average:>12.6f}"
        )

    lines.extend(
        [
            "",
            "Проверка результатов:",
            "Для каждого размера содержимое файлов результатов всех семи методов должно совпадать.",
            "Файлы результатов находятся в папке time_results.",
            "",
            "Выводы:",
            "Заполните этот раздел после просмотра таблицы: укажите, какие методы оказались",
            "быстрее на ваших данных и как изменилось время при увеличении размера массива.",
        ]
    )

    return "\n".join(lines) + "\n"


def update_tests_file(report):
    """Добавляет таблицу в конец tests.txt, сохраняя прежние тесты.

    При повторном запуске старый блок замеров ЛР4 заменяется новым,
    а не дублируется.
    """
    if TESTS_FILE.exists():
        old_text = TESTS_FILE.read_text(encoding="utf-8")
    else:
        old_text = ""

    block = START_MARKER + "\n" + report + END_MARKER + "\n"

    start = old_text.find(START_MARKER)
    end = old_text.find(END_MARKER)

    if start != -1 and end != -1 and end >= start:
        end += len(END_MARKER)
        updated = old_text[:start].rstrip() + "\n\n" + block
        updated += old_text[end:].lstrip("\r\n")
    else:
        updated = old_text.rstrip()
        if updated:
            updated += "\n\n"
        updated += block

    TESTS_FILE.write_text(updated, encoding="utf-8")


def check_results(count):
    """Проверяет, что все семь алгоритмов дали одинаковый отсортированный массив."""
    contents = []
    for method in METHODS:
        path = RESULTS_DIR / f"result_{count}_{method}.txt"
        if not path.exists():
            raise RuntimeError(f"Не найден файл результата: {path.name}")
        contents.append(path.read_text(encoding="utf-8").strip())

    if any(content != contents[0] for content in contents[1:]):
        raise RuntimeError(
            f"Результаты сортировок для {count} элементов различаются. "
            "Проверьте алгоритмы; таблица времени не будет считаться завершённой."
        )


def main():
    if not PROGRAM.exists():
        print(
            "Ошибка: рядом с measure_time.py не найден файл laba_4.py. "
            "Положите measure_time.py в корневую папку проекта.",
            file=sys.stderr,
        )
        return 1

    RESULTS_DIR.mkdir(exist_ok=True)

    try:
        create_input_files()
        rows = []
        total = len(SIZES) * len(METHODS) * REPEATS
        current = 0

        print("\nИзмеряю время сортировок...")
        for count in SIZES:
            input_file = PROJECT_DIR / f"data_{count}.txt"

            for method in METHODS:
                output_file = RESULTS_DIR / f"result_{count}_{method}.txt"
                times = []

                for repeat in range(1, REPEATS + 1):
                    current += 1
                    elapsed = measure_one(input_file, output_file, method)
                    times.append(elapsed)
                    print(
                        f"[{current}/{total}] {count} элементов, "
                        f"{method}, запуск {repeat}: {elapsed:.6f} с"
                    )

                rows.append((count, method, times))

            check_results(count)
            print(f"Результаты всех методов для {count} элементов совпадают.\n")

        report = make_report(rows)
        REPORT_FILE.write_text(report, encoding="utf-8")
        update_tests_file(report)

    except (OSError, RuntimeError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    print(f"Готово! Таблица времени сохранена в файле: {REPORT_FILE.name}")
    print(f"Та же таблица добавлена в конец {TESTS_FILE.name}; прежние тесты сохранены.")
    print(f"Файлы результатов сохранены в папке: {RESULTS_DIR.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
