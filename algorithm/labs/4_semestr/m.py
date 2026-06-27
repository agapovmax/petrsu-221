import sys

def solve():
    data = sys.stdin.read().split()
    idx = 0
    n, m = int(data[idx]), int(data[idx+1])
    idx += 2

    a = [int(data[idx+i]) for i in range(n)]
    idx += n

    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[py] = px

    for _ in range(m):
        d1, d2 = int(data[idx]) - 1, int(data[idx+1]) - 1
        idx += 2
        union(d1, d2)

    # For each component, find the node with minimum price
    comp_min = {}
    for i in range(n):
        root = find(i)
        if root not in comp_min or a[i] < comp_min[root][0]:
            comp_min[root] = (a[i], i)

    components = list(comp_min.values())

    if len(components) == 1:
        print(0)
        return

    # Connect all components via star at global minimum node
    # (optimal since edge cost = a[i]+a[j]: star minimizes total cost)
    _, global_min_node = min(components)

    result = []
    for val, node in components:
        if node != global_min_node:
            result.append((global_min_node + 1, node + 1))

    print(len(result))
    for u, v in result:
        print(u, v)

solve()
