'''Имеется массив целых чисел numbers. Необходимо найти все последовательности в массиве (подряд стоящие числа), сумма которых равна заданному числу S.

Пример: nums = [4,-1,7,0,1,2,-1,5], S = 3, последовательности: [4, -1], [0, 1, 2], [1, 2]'''

numbers = [4,-1,7,0,1,2,-1,5]
s = 3
uniq = []

# for i in range(len(numbers)):
#     print(i)
#     if (numbers[i]+numbers[i+1] == s) and (i+1<=len(numbers)) :
#         print(numbers[i], numbers[i+1], "\t", i)
#         uniq.append([numbers[i], numbers[i+1]])
#     else:
#         continue
# print(uniq)

# for i in range(len(numbers)):
#     print(i)
#     for k in range(1, len(numbers)):
#         print(numbers[i], numbers[k])
#         if numbers[i]+numbers[k] == s:
#             uniq.append([numbers[i], numbers[k]])
#     else:
#         continue
# print(uniq)

i = 0
t=0
while i < (len(numbers)):
    print(i, t)
    while t <=i:
        t+=1
    #t+=1
    i+=1


#print(uniq)