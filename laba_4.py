import sys
from math import*
from calc.arrays import MIN_VALUE, MAX_VALUE, MAX_COUNT
from calc.arrays import binary_search, generate_array
from calc.sorting import METHODS

def pokazat_spravku():
    """Выводит справку о назначении программы и способах её запуска."""
    # Печатаем описание программы и доступные команды в стандартный поток вывода.
    # Используем тройные кавычки для многострочной строки — это удобно для длинного текста.
    print("mathtool — решение уравнений вида A*x^2 + B*x + C = 0")
    print()
    print("Использование:")
    print("    python laba_4.py                         вывод общей справки")
    print("    python laba_4.py --help                   вывод общей справки")
    print("    puthon laba_4.py <команда> --help           справка по команде")
    print("    python laba_4.py solve                    ввод коэффициентов с клавиатуры")
    print("    python laba_4.py solve -a 1 -b -3 -c 2    решение с заданными коэффициентами")
    print("    python laba_4.py stats --input number.txt  показатели последовательности")
    print("    python laba_4.py series --func sqplus --terms 6")
    print("    python laba_4.py series --func sqplus --eps 0.0001")
    print("    python laba_4.py integrate --func ratio --from 0 --to 20 --steps 1000")
    print("    python laba_4.py fill --c 20 --min -10 --max 10 --seed 1 --o small.txt генерация случ. чисел")
    print("    python laba_4.py sort --m counting --i small.txt -o sorted.txt      сортировка")
    print("    python laba_4.py search -v 5 -i sorted.txt")

    print()
    print("Коэффициенты A, B, C — целые числа, по модулю не превышающие 10000.")
#если аргументов нет или введена команда --help
#показываем справку
if len(sys.argv)==1 or sys.argv[1]=='--help':
    pokazat_spravku()

from cli import main

if __name__ == "__main__":
    main()