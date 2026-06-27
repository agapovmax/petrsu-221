from collections import deque

# Чтение входных данных
n, m, start = map(int, input().split())

# Список смежности (индексация с 1)
graph = [[] for _ in range(n + 1)]

# Чтение рёбер
for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)  # неориентированный граф

# Для детерминированного порядка обхода — сортируем соседей
for i in range(1, n + 1):
    graph[i].sort()

# BFS (волновой обход)
visited = [False] * (n + 1)
order = []  # порядок посещения вершин
queue = deque()

visited[start] = True
queue.append(start)

while queue:
    curr = queue.popleft()
    order.append(curr)
    
    for neighbor in graph[curr]:
        if not visited[neighbor]:
            visited[neighbor] = True
            queue.append(neighbor)

# Вывод результата
print(len(order))
print(' '.join(map(str, order)))