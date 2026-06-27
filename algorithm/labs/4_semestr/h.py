from collections import deque

n, m = map(int, input().split())

adj = [[] for _ in range(n + 1)]

for _ in range(m):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

comp = [0] * (n + 1)
num = 0

for start in range(1, n + 1):
    if comp[start] == 0:
        num += 1
        q = deque([start])
        comp[start] = num
        while q:
            v = q.popleft()
            for u in adj[v]:
                if comp[u] == 0:
                    comp[u] = num
                    q.append(u)

print(num)
print(*comp[1:])
