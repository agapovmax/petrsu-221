import sys

data = sys.stdin.buffer.read().split()
idx = 0

n = int(data[idx]); idx += 1

MAXN = 1000001
stack     = [0] * MAXN
max_stack = [0] * MAXN
top = 0

out = []

for _ in range(n):
    op = data[idx]; idx += 1

    if op == b'1':
        x = int(data[idx]); idx += 1
        stack[top] = x
        max_stack[top] = x if top == 0 else (x if x > max_stack[top - 1] else max_stack[top - 1])
        top += 1

    elif op == b'2':
        out.append(max_stack[top - 1])

    elif op == b'3':
        out.append(stack[top - 1])

    else:  # op == b'4'
        top -= 1

sys.stdout.write('\n'.join(map(str, out)))
