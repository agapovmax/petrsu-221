import sys
import random
input = sys.stdin.readline

n = int(input())
numbers = list(map(int, input().split()))

def partition(arr, low, high):
    pivot = arr[(low + high) // 2]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while arr[i] > pivot:
            i += 1
        j -= 1
        while arr[j] < pivot:
            j -= 1
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]

def quicksort(arr, low, high):
    stack = [(low, high)]
    while stack:
        low, high = stack.pop()
        if low < high:
            p = partition(arr, low, high)
            stack.append((low, p))
            stack.append((p + 1, high))

random.shuffle(numbers)
quicksort(numbers, 0, len(numbers) - 1)
print(*numbers)
