#include <stdio.h>
#include <stdlib.h> // надо проверить, нужен ли abs для gcd (gcd кстати есть в c++)
#include "rational.h"

// Алгоритм Евклида, для поиска наибольшего общего делителя. Делим числитель на знаменатель пока остаток от деления с не станет 0. Если нет остатка - это НОД, если есть, то большее число заменяем на остаток от деления.
long gcd(long num, long denom) {
    long c=0;

    while (denom!=0) {
        printf("До сокращения num=%ld, denom=%ld\n", num, denom); 
	    c = num % denom;
        num = denom;
	    denom = c;
        printf("num=%ld, denom=%ld, c=%ld\n", num, denom, c); 
    }

    return labs(num); // иначе в abs не влезет http://all-ht.ru/inf/prog/c/func/abs,labs,llabs.html
    // Функция labs рассчитывает абсолютное значение (модуль) 32-х разрядного целого числа. Отличие от функции abs в типе аргумента и возвращаемого значения. В функции labs используется тип long, который всегда 32 разрядный, не зависимо от архитектуры процессора.
}

// Функция сокращения дроби из двух чисел типа long - одного reduct типа rational_t
rational_t rational(long numerator, long denominator) {
    if (numerator < 0) {
        printf("Числитель меньше нуля!\n");
	    numerator = numerator*(-1);
        denominator = denominator*(-1);
    }

    // Переменная для сокращенной дроби типа rational_t
    rational_t reduct;

    // Приводим числа 0 или 0/n к виду 0/1
    if (numerator == 0) {
        printf("Числитель равен нулю!\n");
	    reduct.num = 0;
	    reduct.denom = 1;
    }

    // Приводим числа n/0 к виду 0/0
    // if (denominator == 0) {
	//     //printf("Неверный формат\n");
    //     reduct.num = 0;
	//     reduct.denom = 1;
    // }

    // Избавляемся от знака в числителе numerator
    //if (numerator < 0) {
	//    numerator = numerator*(-1);
    //    denominator = denominator*(-1);
    //}
    
    // Переменная для наибольшего общего делителя (100% попадание в int при abs)
    unsigned long nod = gcd(numerator, denominator);
    
    // Делим числитель и знаменатель на НОД и возвращаем сокращенную дробь reduct
    printf("НОД=%ld\n", nod);
    reduct.num = numerator/nod;
    reduct.denom = denominator/nod;

    printf("%ld\t%ld\n", reduct.num, reduct.denom);

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