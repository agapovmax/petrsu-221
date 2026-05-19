# Ввод данных из консоли
n = int(input())
A = list(map(int, input().split()))
 
max_sum = A[0]      # Максимальная сумма
current_sum = A[0]  # Текущая сумма
 
start = end = 0  # Начальный и последний индекс подпоследовательности
temp_start = 0  # Временная переменная ждя текущей подпоследовательности
 
for i in range(1, n):
    # Если текущая сумма + новый элемент меньше, чем просто новый элемент,
    # начинаем новую подпоследовательность
    if current_sum + A[i] < A[i]:
        current_sum = A[i]
        temp_start = i
    else:
        current_sum += A[i]
 
    # Обновляем максимум
    if current_sum > max_sum:
        max_sum = current_sum
        start = temp_start
        end = i
 
# Результат (индексы с 1)
print(max_sum)
print(start + 1, end + 1)