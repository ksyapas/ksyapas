from sys import*
from math import*

def pokazat_spravku():
    """Выводит справку о назначении программы и способах её запуска."""
    # Печатаем описание программы и доступные команды в стандартный поток вывода.
    # Используем тройные кавычки для многострочной строки — это удобно для длинного текста.
    print("mathtool — решение уравнений вида A*x^2 + B*x + C = 0")
    print()
    print("Использование:")
    print("    python laba_2.py                         вывод общей справки")
    print("    python laba_2.py --help                   вывод общей справки")
    print("    puthon laba_2.py <команда> --help           справка по команде")
    print("    python laba_2.py solve                    ввод коэффициентов с клавиатуры")
    print("    python laba_2.py solve -a 1 -b -3 -c 2    решение с заданными коэффициентами")
    print("    python laba_2.py stats --input number.txt  показатели последовательности")
    print("    python laba_2.py series --func sqplus --terms 6")
    print("    python laba_2.py series --func sqplus --eps 0.0001")
    print("    python laba_2.py integrate --func ratio --from 0 --to 20 --steps 1000")
    print()
    print("Коэффициенты A, B, C — целые числа, по модулю не превышающие 10000.")
#если аргументов нет или введена команда --help
#показываем справку
if len(argv)==1 or argv[1]=='--help':
    pokazat_spravku()


from cli import main

if __name__ == "__main__":
    main()
