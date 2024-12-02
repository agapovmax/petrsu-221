#ifndef RATIO_H
#define RATIO_H
#include "rational.h"
// Функция ввод чисел
void input_rational(char *chlen1, char *chlen2, char operator);
// Калькулон
void math_rational(rational_t ch1, rational_t ch2, char operator);
// Функция перевода строки в рациональное число
rational_t str_to_rational(char *chlen);
#endif