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
        int n,m,k,c,i;
		printf("Укажите начало диапазона n: ");
        scanf("%d", &n);
		printf("Укажите конец диапазона m: ");
        scanf("%d", &m);
		//Собираем все простые числа в этом диапазоне
        calculate_primes (primes, m);
		//Начинаем проверять четные числа от k (оно же начальное значение диапазона n)
        for (k=n; k<=m; k=k+2) {
            // счетчик для количества разложений
            c=0;
			//Проверяем, если k-индекс И i-индекс не простые числа. Иначе это число - не сумма простых чисел
            //k - это как раз произведение двух простых чисел, его можно представить как k\2. Считаем до минимального множителя
            for (i=2; i<=k/2; i++) {
                if ((primes[k-i]!=0) && (primes[i]!=0))
                    //пополняем общее количество разложений
					c++;
                }
            //выводим множители
            for (i=2; i<=k/2; i++) {
                if ((primes[k-i]!=0) && (primes[i]!=0)) {
                    printf("%d %d %d %d\n", k, c, i, k-i);
                    break;
                }
            }
        }
    return 0;
}