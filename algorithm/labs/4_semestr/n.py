import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1

    SIZE  = 2_000_003  # простое > 2*10^6
    SIZE2 = 1_999_979  # второе простое для двойного хеширования
    _DEL = object()
    tbl: list = [None] * SIZE

    out = []
    _append = out.append
    _Yes = b"Yes"
    _No = b"No"

    for _ in range(n):
        op = data[pos]; pos += 1
        x = int(data[pos]); pos += 1
        h    = x % SIZE
        step = 1 + (abs(x) % SIZE2)   # шаг уникален для каждого x → нет кластеризации

        if op == b'1':          # добавить
            fd = -1
            while True:
                v = tbl[h]
                if v is None:
                    tbl[fd if fd >= 0 else h] = x
                    break
                if v == x:
                    break
                if v is _DEL and fd < 0:
                    fd = h
                h = (h + step) % SIZE

        elif op == b'2':        # проверить
            found = False
            while True:
                v = tbl[h]
                if v is None:
                    break
                if v == x:
                    found = True
                    break
                h = (h + step) % SIZE
            _append(_Yes if found else _No)

        else:                   # удалить
            while True:
                v = tbl[h]
                if v is None:
                    break
                if v == x:
                    tbl[h] = _DEL
                    break
                h = (h + step) % SIZE

    sys.stdout.buffer.write(b"\n".join(out))
    if out:
        sys.stdout.buffer.write(b"\n")

main()
