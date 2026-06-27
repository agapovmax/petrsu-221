import math

def solve():
    n = int(input())
    coords = []
    for _ in range(n):
        x, y = map(int, input().split())
        coords.append((x, y))

    if n == 1:
        print("0.000000000")
        return

    # Prim's O(n^2): maintain min distance from each node to the growing MST
    dist = [float('inf')] * n
    in_mst = [False] * n
    dist[0] = 0.0
    total = 0.0

    for _ in range(n):
        # pick the nearest non-MST node
        u = -1
        for v in range(n):
            if not in_mst[v] and (u == -1 or dist[v] < dist[u]):
                u = v

        in_mst[u] = True
        total += dist[u]

        # relax distances to remaining nodes
        xu, yu = coords[u]
        for v in range(n):
            if not in_mst[v]:
                dx = xu - coords[v][0]
                dy = yu - coords[v][1]
                d = math.sqrt(dx * dx + dy * dy)
                if d < dist[v]:
                    dist[v] = d

    print(f"{total:.9f}")

solve()
