n = int(input())
numbers = list(map(int, input().split()))

def merge_sort(numbers):
    # Базовый случай: если массив состоит из 1 элемента, он уже отсортирован
    if len(numbers) <= 1:
        return numbers
    
    # 1. Делим массив пополам
    mid = len(numbers) // 2
    left_half = numbers[:mid]
    right_half = numbers[mid:]
    
    # 2. Рекурсивно сортируем обе половины
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)
    
    # 3. Сливаем две отсортированные половины
    return merge(left_sorted, right_sorted)

def merge(left, right):
    result = []
    i = j = 0
    
    # Сравниваем элементы из левого и правого списков и берем меньший
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Добавляем оставшиеся элементы (если один список закончился раньше)
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

print(*merge_sort(numbers))