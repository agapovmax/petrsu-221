"""
Задача о нарезке бельевых веревок

Решение через бинарный поиск по ответу:
- Ищем максимальную длину веревочки, из которой можно нарезать K штук
- Проверяем, можно ли из имеющихся веревок нарезать K кусков длиной mid
"""

# Чтение входных данных
n, k = map(int, input().split())

ropes = []
for _ in range(n):
    length = int(input())
    ropes.append(length)

# Решение задачи
if n == 0 or k == 0:
    print(0)
else:
    # Бинарный поиск по ответу
    left = 0
    right = max(ropes) if ropes else 0
    answer = 0

    # Используем целочисленный бинарный поиск
    while left <= right:
        mid = (left + right) // 2

        # Проверяем, можно ли нарезать k кусков длиной mid
        if mid == 0:
            can_cut_result = True
        else:
            total = sum(rope // mid for rope in ropes)
            can_cut_result = total >= k

        if can_cut_result:
            answer = mid
            left = mid + 1  # Пробуем найти больше
        else:
            right = mid - 1  # Уменьшаем длину

    # Вывод результата
    print(answer)
