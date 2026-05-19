n = int(input())
a = list(map(int, input().split()))
q = int(input())
 
p = [0]
for i in range(n):
    p.append(p[i] + a[i])
 
for i in range(q):
    l, r = map(int, input().split())
    print(p[r] - p[l - 1])