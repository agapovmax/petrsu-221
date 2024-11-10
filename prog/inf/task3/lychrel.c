/**
 * "lychrel.c -- ненавижу"
 *
 * Copyright (c) 2024, Max Agapov <mtagapov@cs.petrsu.ru>
 *
 * This code is licensed under MIT license.
 */

#include <stdio.h>
#include <limits.h>

/* Выводит все кандидаты в числа Лишрел из отрезка
   1, 2, ..., last_number */
void show_lychrel_candidates(long last_number);

/* Проверяет, является ли number кандидатом в числа Лишрел */
int is_lychrel_candidate(long number);

/* Возвращает обращение числа n */
long reverse(long n);

/* Основная функция */
int main()
{
    /* Получаем значение верхней границы последовательности */
    long last_number;
    printf("Введите верхнюю границу отрезка поиска чисел Лишрел: ");
    scanf("%ld", &last_number);

    /* Выводим все кандидаты в числа Лишрел до last_number */
    show_lychrel_candidates(last_number);

    return 0;
}

void show_lychrel_candidates(long last_number)
{
    long number;

    /* Проверим каждое число в заданном отрезке: */
    for (number = 1; number <= last_number; number++) {
        /* Если оно является кандидатом в числа Лишрел, напечатаем его */
        if (is_lychrel_candidate(number)) {
        //    printf("%ld\n", number);
        }
    }
}

int is_lychrel_candidate(long number)
{
    long n = number;
    long r = reverse(n);

    /* Повторяем ... */
    do {
        /* Если сумма числа и его обращения n = n + r (786 = 195+591) переполняет разрядную сетку, */
        if ((r == -1) || (n > LONG_MAX - r)) {
            // 786 > LONG_MAX - 591
            /* то считаем число искомым кандидатом и завершаем проверку */
            printf("Число в кандидаты Лишрел: ");
            /* то считаем число искомым кандидатом и завершаем проверку */
            return 1;
        }
        /* иначе вычисляем новое значение, складывая число с обращением */
        n = n + r;

        /* Вычисляем обращение суммы */
        r = reverse(n);

    /* ... пока число не совпадает с обращением */
    } while (n != r);

    /* Считаем, что проверяемое число - не число Лишрел и завершаем проверку */
    return 0;
}

long reverse(long n)
{
    long r = 0;
    /* Кто такой вообще этот ваш LONG_MAX?*/

    do {
        /* Проверяем переполнение
         Так как r (оборотное число) не сможет принять значение больше LONG_MAX, перед операцией обращения числа, необходимо выполнить проверку
	    */
        if (r > LONG_MAX / 10 - n % 10) {
                return -1;
        }
        r = r * 10 + n % 10;
        n /= 10;

    } while (n > 0);

    return r;

}
