/**
 * calculate_primes.c - функция заполнения массива простыми числами
 * 
 * Copyright (c) 2024, Max Agapov <mtagapov@cs.petrsu.ru>
 *
 * This code is licensed under MIT license.
 */

#include <stdio.h>

/* Функция построения массива индикаторов */
void calculate_primes(int *primes, int n) {

    // Готовим массив с первого простого числа - двойки
    primes[2] = 1;
    printf("%d", primes[3]);

    for (int i=3; i<=n; i++) {
        // Индикатор принадлежности числа к простому (1 - да, 0 - нет). По-умолчанию не простое
        int s=0;
        // Перебираем числа дальше чтобы каждое делить на это число
        for (int j=2; j<i; j++) {
            // Если делится без остатка - не простое число и меняем индикатор на 1
            if (i%j == 0) {
                s=1;
                break;
            }
        }
        // Если индикатор не поменялся - это наш клиент
        if (s == 0) {
            primes[i]=1;
        }
    }
}