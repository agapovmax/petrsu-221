/*
 * Калькулон - калькулятор рациональных чисел
 * 
 * Copyright (c) 2024, Max Agapov <mtagapov@cs.petrsu.ru>
 *
 * This code is licensed under MIT license.
 */

#include <stdio.h>
#include "rational/rat_io.h"

int main(void) {
    
    // строковый массив для первого рационального числа (11 символов) и для второго (10 символов)
    char exp1[26], exp2[26];
    // символ для оператора (1)
    char op;

    while(1) {
        scanf("%s %c %s", exp1, &op, exp2);
        // Калькуляция
        input_rational(exp1, exp2, op);
    }

    return 0;
}