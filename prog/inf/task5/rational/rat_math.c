#include <stdio.h>
#include "rat_math.h" // прототипы функций rat_*

// Функция суммирования
rational_t rat_add(rational_t a, rational_t b) {
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