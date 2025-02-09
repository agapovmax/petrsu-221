/**
 * goldbach.c -- программа вычисления суммы четного числа из двух простых
 *
 * Copyright (c) 2024, Max Agapov <mtagapov@cs.petrsu.ru>
 *
 * This code is licensed under MIT license.
 */

#include <stdio.h>
#include "calculate_primes.c"

void calculate_primes (int *primes, int n);

int primes[10000000];

int main () {

        int n,m,k,c,i,s;

		printf("Укажите начало диапазона n: ");
        scanf("%d", &n);
		printf("Укажите конец диапазона m: ");
        scanf("%d", &m);
		// Собираем все простые числа в этом диапазоне
        calculate_primes (primes, m);
		// Начинаем проверять четные числа от k (оно же начальное значение диапазона n)
        for (k=n; k<=m; k=k+2) {
            // Счетчик для количества разложений
            c=0;
			// Проверяем, если k-индекс И i-индекс не простые числа. Иначе это число - не сумма простых чисел
            // Если число k можно представить как сумму двух простых чисел x и y, то необходимо проверить только до половины k, потому что комбинации чисел симметричны
            // Проверка до k/2 снижает количество итераций
            for (i=2; i<=k/2; i++) {
                if ((primes[k-i]!=0) && (primes[i]!=0))
                    // Пополняем общее количество разложений
					c++;
                    if (c==1)
                        s = i;        
                }
            // Выводим множители
            printf("%d %d %d %d\n", k, c, s, k-s);
       }
    return 0;
}