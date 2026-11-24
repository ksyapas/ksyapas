from calc.arrays import MIN_VALUE, MAX_VALUE

def bubble_sort(values, descending=False):
    #Сортируем список пузырьковым методом
    n=len(values)
    for i in range (n-1):
        for j in range (n-1-i):
            if descending:
                #по убыванию
                if values[j]<values[j+1]:
                    values[j], values[j+1]=values[j+1], values[j]
            else:
                #по возрастанию
                if values[j]>values[j+1]:
                    values[j], values[j+1]=values[j+1], values[j]

def selection_sort(values, descending=False):
    #Сортирует список методом выбора
    n=len(values)
    for i in range (n-1):
        selected=i
        for j in range (i+1, n):
            if descending:
                if values[j]>values[selected]:
                    selected=i
            else:
                if values[j]<values[selected]:
                    selected=j
        values[i], values[selected]=values[selected], values[i]

def insertion_sort(values, descending=False):
    #Сортирует список методом вставок
    n=len(values)
    for i in range (1, n):
        key=values[i]
        j=i-1
        if descending:
            while j>=0 and values[j]<key:
                values[j+1]=values[j]
                j-=1
        else:
            while j>=0 and values[j]>key:
                values[j+1]=values[j]
                j-=1
        values[j+1]=key

def counting_sort(values, descending=False):
    #Сортирует список методом подсчета
    counts=[0]*(MAX_VALUE-MIN_VALUE+1)
    for number in values:
        counts[number-MIN_VALUE]+=1
    index=0
    if descending:
        numbers_range=range(MAX_VALUE, MIN_VALUE-1, -1)
    else:
        numbers_range=range(MIN_VALUE, MAX_VALUE+1)
    for number in numbers_range:
        count=counts[number-MIN_VALUE]
        for _ in range(count):
            values[index]=number
            index+=1

METHODS={
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "counting": counting_sort,
}