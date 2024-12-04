#include <stdio.h>
#include "rational.h"

// Алгоритм Евклида, для поиска наибольшего общего делителя. Делим числитель на знаменатель пока остаток от деления с не станет 0. Если нет остатка - это НОД, если есть, то большее число заменяем на остаток от деления.
long gcd(unsigned long num, unsigned long denom) {
    unsigned long c;

    while (denom!=0) {
    //  printf("ДО ВЫЧИСЛЕНИЯ НОД: num=%lu, denom=%lu, c=%lu\n", num, denom, c);     // ОТЛАДКА 
	    c = num % denom;
        num = denom;
	    denom = c;
    //  printf("num=%lu, denom=%lu, c=%lu\n", num, denom, c);   // ОТЛАДКА
    }

    return num;
}

// Функция сокращения дроби
rational_t rational(unsigned long numerator, unsigned long denominator) {

    // Переменная для сокращенной дроби типа rational_t
    rational_t reduct;

    // Переменная для наибольшего общего делителя (100% попадание в int при abs)
    unsigned long nod = gcd(numerator, denominator);
    
    // Делим числитель и знаменатель на НОД и возвращаем сокращенную дробь reduct
    //printf("%lu/%lu\n", numerator, nod);        // ОТЛАДКА
    //printf("%lu/%lu\n", denominator, nod);      // ОТЛАДКА
    
    reduct.num = numerator/nod;
    reduct.denom = denominator/nod;
    //printf("%lu\t%lu\n", reduct.num, reduct.denom);   // ОТЛАДКА

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
