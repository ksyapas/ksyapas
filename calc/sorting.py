from calc.arrays import MIN_VALUE, MAX_VALUE

def before(a, b, descending=False):
    if descending:
        return a > b
    else:
        return a < b

#Сортирровка пузырьком
def bubble_sort(values, descending=False):
    n = len(values)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if before(values[j + 1], values[j], descending):
                values[j], values[j + 1] = values[j + 1], values[j]

#Сортировка выбором
def selection_sort(values, descending=False):
    n = len(values)
    for i in range(n - 1):
        selected = i

        for j in range(i + 1, n):
            if before(values[j], values[selected], descending):
                selected = j

        values[i], values[selected] = values[selected], values[i]

#Сортировка вставками
def insertion_sort(values, descending=False):
    n = len(values)
    for i in range(1, n):
        key = values[i]
        j = i - 1
        while j >= 0 and before(key, values[j], descending):
            values[j + 1] = values[j]
            j -= 1
        values[j + 1] = key

#Сортировка подсчетом
def counting_sort(values, descending=False):
    counts = [0] * (MAX_VALUE - MIN_VALUE + 1)
    for number in values:
        counts[number - MIN_VALUE] += 1
    index = 0
    if descending:
        numbers_range = range(MAX_VALUE, MIN_VALUE - 1, -1)
    else:
        numbers_range = range(MIN_VALUE, MAX_VALUE + 1)

    for number in numbers_range:
        count = counts[number - MIN_VALUE]

        for _ in range(count):
            values[index] = number
            index += 1

#Быстрая сортировка
def quick(values, descending=False):
    _quick_sort(values, 0, len(values) - 1, descending)

def _quick_sort(values, left, right, descending):
    while left < right:
        pivot = values[(left + right) // 2]

        i = left
        j = right

        while i <= j:
            while before(values[i], pivot, descending):
                i += 1

            while before(pivot, values[j], descending):
                j -= 1

            if i <= j:
                values[i], values[j] = values[j], values[i]
                i += 1
                j -= 1

        if j - left < right - i:
            if left < j:
                _quick_sort(values, left, j, descending)
            left = i
        else:
            if i < right:
                _quick_sort(values, i, right, descending)
            right = j

#Сортировка слиянием     
def merge(values, descending=False):
    _merge_sort(values, 0, len(values) - 1, descending)

def _merge_sort(values, left, right, descending):
    if left >= right:
        return

    middle = (left + right) // 2

    _merge_sort(values, left, middle, descending)
    _merge_sort(values, middle + 1, right, descending)

    _merge(values, left, middle, right, descending)

def _merge(values, left, middle, right, descending):
    result = []

    i = left
    j = middle + 1

    while i <= middle and j <= right:
        if before(values[j], values[i], descending):
            result.append(values[j])
            j += 1
        else:
            result.append(values[i])
            i += 1

    while i <= middle:
        result.append(values[i])
        i += 1

    while j <= right:
        result.append(values[j])
        j += 1

    values[left:right + 1] = result

#Пирамидальная сортировка
def heap(values, descending=False):
    n = len(values)

    def sift_down(size, root):
        while True:
            selected = root
            left = 2 * root + 1
            right = 2 * root + 2

            if left < size and before(values[selected], values[left], descending):
                selected = left

            if right < size and before(values[selected], values[right], descending):
                selected = right

            if selected == root:
                break

            values[root], values[selected] = values[selected], values[root]
            root = selected

    for i in range(n // 2 - 1, -1, -1):
        sift_down(n, i)

    for i in range(n - 1, 0, -1):
        values[0], values[i] = values[i], values[0]
        sift_down(i, 0)

METHODS = {
"bubble": bubble_sort,
"selection": selection_sort,
"insertion": insertion_sort,
"counting": counting_sort,
"quick": quick,
"merge": merge,
"heap": heap,
}