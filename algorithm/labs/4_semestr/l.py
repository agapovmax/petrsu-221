import sys
input = sys.stdin.readline

MAXN = 1_000_002

node_val = [0] * MAXN  # value stored at node i
nxt      = [0] * MAXN  # next node index  (0 = none)
prv      = [0] * MAXN  # prev node index  (0 = none)
pos      = [0] * MAXN  # pos[v] = node index for value v

head = [0]  # mutable head/tail/cnt via single-element list
tail = [0]
cnt  = [0]


def new_node(v):
    cnt[0] += 1
    i = cnt[0]
    node_val[i] = v
    pos[v] = i
    nxt[i] = prv[i] = 0
    return i


def add_end(v):
    i = new_node(v)
    if tail[0] == 0:
        head[0] = tail[0] = i
    else:
        nxt[tail[0]] = i
        prv[i] = tail[0]
        tail[0] = i


def add_begin(v):
    i = new_node(v)
    if head[0] == 0:
        head[0] = tail[0] = i
    else:
        nxt[i] = head[0]
        prv[head[0]] = i
        head[0] = i


def delete_val(v):
    i = pos[v]
    if i == 0:
        return
    p = prv[i]
    n = nxt[i]
    if p:
        nxt[p] = n
    else:
        head[0] = n
    if n:
        prv[n] = p
    else:
        tail[0] = p
    pos[v] = 0


def insert_after(x, y):
    y_node = pos[y]
    if y_node == 0:
        return
    x_node = new_node(x)
    n = nxt[y_node]
    nxt[y_node] = x_node
    prv[x_node] = y_node
    nxt[x_node] = n
    if n:
        prv[n] = x_node
    else:
        tail[0] = x_node


def solve():
    q = int(input())
    out = []
    for _ in range(q):
        parts = input().split()
        op = parts[0]
        if op == '1':
            add_end(int(parts[1]))
        elif op == '2':
            add_begin(int(parts[1]))
        elif op == '3':
            delete_val(int(parts[1]))
        elif op == '4':
            insert_after(int(parts[1]), int(parts[2]))
        else:  # op == '5'
            v = int(parts[1])
            i = pos[v]
            if i == 0:
                out.append("end")
            else:
                n = nxt[i]
                out.append("end" if n == 0 else str(node_val[n]))
    sys.stdout.write('\n'.join(out) + ('\n' if out else ''))


solve()
