import sys

data = sys.stdin.buffer.read().split()
idx = 0

MAXN = 1000002

heap = [0] * MAXN
heap_size = 0

out_list = []

while idx < len(data):
    op = data[idx]; idx += 1

    if op == b'add':
        x = int(data[idx]); idx += 1
        heap[heap_size] = x
        i = heap_size
        heap_size += 1
        # sift up
        while i > 0:
            parent = (i - 1) >> 1
            if heap[parent] < heap[i]:
                heap[parent], heap[i] = heap[i], heap[parent]
                i = parent
            else:
                break

    else:  # remove
        if heap_size == 0:
            out_list.append(b'ERROR')
        else:
            out_list.append(str(heap[0]).encode())
            heap_size -= 1
            heap[0] = heap[heap_size]
            # sift down
            i = 0
            while True:
                left  = 2 * i + 1
                right = 2 * i + 2
                largest = i
                if left  < heap_size and heap[left]  > heap[largest]:
                    largest = left
                if right < heap_size and heap[right] > heap[largest]:
                    largest = right
                if largest != i:
                    heap[largest], heap[i] = heap[i], heap[largest]
                    i = largest
                else:
                    break

sys.stdout.buffer.write(b'\n'.join(out_list))
if out_list:
    sys.stdout.buffer.write(b'\n')
