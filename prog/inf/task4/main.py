import ctypes   # https://docs.python.org/3/library/ctypes.html

# Загрузка скомпилированной библиотеки
lib = ctypes.CDLL('./libcalculate.so')

# Определение функции calculate_primes
# void calculate_primes (int *primes, int n);

#lib.calculate_primes.argtypes = [ctypes.c_int, ctypes.c_int]
lib.calculate_primes.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
lib.calculate_primes.restype = ctypes.c_int # https://docs.python.org/3/library/ctypes.html#ctypes.c_int


def calculate_primes(primes, n):
        c_array = (ctypes.c_int * len(primes))(*primes)
        # Вызываем функцию void calculate_primes
        lib.calculate_primes(c_array, n)
        # Возврат массива с результатами
        return list(c_array)

def main():
    primes = [0] * 10000000

    # Ввод для начала и конца диапазона n и m
    n = int(input("Укажите начало диапазона n: "))
    m = int(input("Укажите конец диапазона m: "))

    # Вызов функции для вычисления простых чисел
    primes = calculate_primes(primes, m)

    for k in range(n, m + 1, 2):
        c = 0
        s = 0
        for i in range(2, (k//2) + 1):
            if primes[k-i] != 0 and primes[i] != 0:
                c += 1
                if c == 1:
                    s = i
        print(f"{k} {c} {s} {k-s}")

if __name__ == '__main__':
    main()
