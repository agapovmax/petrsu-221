import sys

data = sys.stdin.buffer.read().split()
idx = 0

n = int(data[idx]); idx += 1

MAXN = 1000001

# Стек IN — для добавления в конец очереди
in_stack = [0] * MAXN
in_max   = [0] * MAXN
in_top   = 0

# Стек OUT — для удаления/чтения из начала очереди
out_stack = [0] * MAXN
out_max   = [0] * MAXN
out_top   = 0

out_list = []

for _ in range(n):
    op = data[idx]; idx += 1

    if op == b'1':
        x = int(data[idx]); idx += 1
        in_stack[in_top] = x
        in_max[in_top] = x if in_top == 0 else (x if x > in_max[in_top - 1] else in_max[in_top - 1])
        in_top += 1

    else:
        # Если out пуст — перекладываем всё из in в out (порядок разворачивается)
        if out_top == 0:
            while in_top > 0:
                in_top -= 1
                x = in_stack[in_top]
                out_stack[out_top] = x
                out_max[out_top] = x if out_top == 0 else (x if x > out_max[out_top - 1] else out_max[out_top - 1])
                out_top += 1

        if op == b'2':
            # Максимум = максимум из обоих стеков
            m = out_max[out_top - 1]
            if in_top > 0 and in_max[in_top - 1] > m:
                m = in_max[in_top - 1]
            out_list.append(m)

        elif op == b'3':
            out_list.append(out_stack[out_top - 1])

        else:  # op == b'4'
            out_top -= 1

sys.stdout.write('\n'.join(map(str, out_list)))
