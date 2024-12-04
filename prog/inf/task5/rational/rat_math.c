#include <stdio.h>
#include "rat_math.h"

// Функция суммирования
rational_t rat_add(rational_t a, rational_t b) {
    //printf("Умножаем числитель a=%ld на знаменатель b=%ld и прибавляем умножение числителя b=%ld на знаменатель a=%ld\t = %ld\n", rational_numerator(a), rational_denominator(b), rational_numerator(b), rational_denominator(a), rational_numerator(a)*rational_denominator(b)+rational_numerator(b)*rational_denominator(a));
    //printf("И делим все это на произведение знаменателей %ld %ld = %ld\n", rational_denominator(a), rational_denominator(b), rational_denominator(a)*rational_denominator(b));
    return rational(rational_numerator(a)*rational_denominator(b)+rational_numerator(b)*rational_denominator(a),
    rational_denominator(a)*rational_denominator(b));
}

// Функция вычитания
rational_t rat_sub(rational_t a, rational_t b) {
    return rational(rational_numerator(a)*rational_denominator(b)-rational_numerator(b)*rational_denominator(a),
    rational_denominator(a)*rational_denominator(b));
}

// Функция умножения
rational_t rat_mul(rational_t a, rational_t b) {
    return rational(rational_numerator(a)*rational_numerator(b),
    rational_denominator(a)*rational_denominator(b));
}

// Функция деления
rational_t rat_div(rational_t a, rational_t b) {
    return rational(rational_numerator(a)*rational_denominator(b),
    rational_denominator(a)*rational_numerator(b));
}
