#include <stdio.h>
#include <stdlib.h> // надо проверить, нужен ли abs для gcd (gcd кстати есть в c++)
#include "rational.h"

// Алгоритм Евклида, для поиска наибольшего общего делителя. Делим числитель на знаменатель пока остаток от деления с не станет 0. Если нет остатка - это НОД, если есть, то большее число заменяем на остаток от деления.
long gcd(long num, long denom) {
    int c;

    while (denom!=0) {
	    c = num % denom;
        num = denom;
	    denom = c;
        printf("num=%d, denom=%d, c=%d\n", num, denom, c); 
    }

    return abs(num);
}

// Функция сокращения дроби из двух чисел типа long - одного reduct типа rational_t
rational_t rational(long numerator, long denominator) {
    
    // Переменная для сокращенной дроби типа rational_t
    rational_t reduct;

    // Приводим числа 0 или 0/n к виду 0/1
    if (numerator == 0) {
	    reduct.num = 0;
	    reduct.denom = 1;
    }

    // Приводим числа n/0 к виду 0/0
    if (denominator == 0) {
	    //printf("Неверный формат\n");
        reduct.num = 0;
	    reduct.denom = 1;
    }

    // Избавляемся от знака в числителе numerator
    if (numerator < 0) {
	    numerator = numerator*(-1);
    }

    // Избавляемся от знака в знаменателе denominator
    if (denominator < 0) {
	    denominator = denominator*(-1);
    }
    
    // Переменная для наибольшего общего делителя (100% попадание в int при abs)
    int nod = gcd(numerator, denominator);
    
    // Делим числитель и знаменатель на НОД и возвращаем сокращенную дробь reduct
    printf("%d/%d\n", numerator, nod);
    printf("%d/%d\n", denominator, nod);
    
    reduct.num = numerator/nod;
    reduct.denom = denominator/nod;

    printf("%d\t%d\n", reduct.num, reduct.denom);

    return reduct;
}

// Функция возвращения числителя дроби
long rational_numerator(rational_t reduct) {
    return reduct.num;
}

// Функция возвращения знаменателя дроби/
long rational_denominator(rational_t reduct) {
    return reduct.denom;
}