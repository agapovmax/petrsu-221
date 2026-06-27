import sys
input = sys.stdin.readline

def dfs(u, adj, match_b, used):
    for v in adj[u]:
        if not used[v]:
            used[v] = True
            if match_b[v] == -1 or dfs(match_b[v], adj, match_b, used):
                match_b[v] = u
                return True
    return False

def solve():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        row = list(map(int, input().split()))
        for v in row:
            if v == 0:
                break
            adj[i].append(v)

    match_b = [-1] * (m + 1)
    result = 0

    for u in range(1, n + 1):
        used = [False] * (m + 1)
        if dfs(u, adj, match_b, used):
            result += 1

    print(result)
    for v in range(1, m + 1):
        if match_b[v] != -1:
            print(match_b[v], v)

solve()
