n = int(input())
a = list(map(int, input().split()))

s = 0
for i in range(n):
    s = s + a[i] * (i + 1) * (n - i)

print(s)
