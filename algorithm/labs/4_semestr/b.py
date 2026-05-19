import sys
n = int(input())
numbers = str(input())

arr=list(map(int, numbers.split()))
for i in range(n):
    swapped = 0
    for j in range(0, n - i - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            swapped = 1
    if swapped == 0:
        break
#print(' '.join(map(str, arr)))
sys.stdout.write(' '.join(map(str, arr)))