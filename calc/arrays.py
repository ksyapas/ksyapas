import random

MIN_VALUE=-100
MAX_VALUE=100
MAX_COUNT=1_000_000
MAX_SEARCH=1000

def generate_array(count, low, high, seed=None):
    #Создает массив случайных целых чисел
    if not 1<=count<=MAX_COUNT:
        raise ValueError("Количество элементов должно быть от 1 до 1000000")
    if not MIN_VALUE<=low<=MAX_VALUE:
        raise ValueError("Минимальное значение должно быть от -100 до 100")
    if not MIN_VALUE<=high<=MAX_VALUE:
        raise ValueError ("Максимальное значение должно быть от -100 до 100")
    if low>high:
        raise ValueError ("Минимальное значение не может быть выше максимального")
    if seed is not None:
        random.seed(seed)
    values=[]
    for _ in range(count):
        number=random.randint(low, high)
        values.append(number)
    return values

def is_sorted(values):
    #Проверяет, отсортирован ли список по возрастанию
    for i in range(len(values)-1):
        if values[i]>values[i+1]:
            return False
    return True

def binary_search(values, target):
    #Ищет элемент в отсортированном списке
    if not is_sorted(values):
        raise ValueError("Список должен быть отсортирован по возрастанию")
    left=0
    right=len(values)-1
    while left<=right:
        middle=(left+right)//2
        if values[middle]==target:
            return middle
        if values[middle]<target:
            left=middle+1
        else:
            right=middle-1
    return None

numbers=[1, 3, 5, 7, 9, 11, 13]
print(binary_search(numbers, 7))
print(binary_search(numbers, 6))