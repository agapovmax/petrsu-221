# Имеется массив целых чисел numbers. Необходимо найти все такие тройки [numbers[i], numbers[j], numbers[k]], где i != j, j != k, k != i и сумма numbers[i] + numbers[j] + numbers[k] = 0

# Пример: nums = [4,-1,7,0,1,2,-1,5], тройки: [[-1,-1,2],[-1,0,1]]

numbers = [4,-1,7,0,1,2,-1,5]
result = []

for i in range(len(numbers)):
    for j in range(len(numbers)):
        for k in range(len(numbers)):
            print('i, j, k',  i, j, k)
            #if (numbers[i] != numbers[j]) and (numbers[j] != numbers[k]) and (numbers[k] != numbers[i]) and (numbers[i] + numbers[j] + numbers[k] == 0):
            if (i != j) and (j != k) and (k != i) and (numbers[i] + numbers[j] + numbers[k] == 0):
                result.append([numbers[i], numbers[j], numbers[k]])
# Вывод найденных троек, но тут могут быть повторения
#print(result)

# Выбираем уникальные значения
uniq =[]
for i in result:
    if i in uniq:
        continue
    else:
        uniq.append(i)
print(uniq)
   