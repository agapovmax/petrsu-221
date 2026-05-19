n = int(input())
numbers = str(input())
 
arr=list(map(int, numbers.split()))
for i in range(1, len(arr)):
    key = arr[i]          # текущий элемент который перемещаем в начало
    j = i - 1             # индекс последнего элемента в отсортированной части

    # Сдвигаем элементы, которые больше key, вправо
    while j >= 0 and arr[j] > key:
        arr[j + 1] = arr[j]
        j -= 1

    # Вставляем ключ на найденное место
    arr[j + 1] = key
print(' '.join(map(str, arr)))