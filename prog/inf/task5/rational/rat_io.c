#include <stdio.h>
#include <string.h>
#include "rat_io.h"
#include "rat_math.h"
#include "rational.h"

// Переменная для последнего введенного значения в виде дроби
rational_t last;

// Калькуляция
void math_rational(rational_t ch1, rational_t ch2, char operator);

// Функция перевода строки в рациональное число*/
rational_t str_to_rational(char *chlen);

// Функция обработки чисел из строки в rational_t перед расчетом на калькуляторе
void input_rational(char *chlen1, char *chlen2, char operator) {
    // Объявляем числа первой и второй дроби
    rational_t ch1, ch2;

    // Конвертируем строковый тип в дробь
    ch1 = str_to_rational(chlen1);
    ch2 = str_to_rational(chlen2);
    
    // Считаем
    math_rational(ch1, ch2, operator);
}

// Операции с числами
void math_rational(rational_t ch1, rational_t ch2, char operator) {
    // Результат будем хранить в переменной с типом rational_t
    rational_t res;

    // Проверяем ввод с консоли на тип операции
    if (operator=='+') {
        res=rat_add(ch1, ch2);
    }
    if (operator=='-') {
        res=rat_sub(ch1, ch2);
    }
    if (operator=='/') {
        res=rat_div(ch1, ch2);
    }
    if (operator=='*') {
        res=rat_mul(ch1, ch2);
    }

    // Сохраняем переменную res в last
    last = res;

    // Выводим результат. В случае если знаменатель результата = 1, то и число выводим как 1
    if (res.denom == 1)
        printf("= %ld\n", res.num);
    else
        printf("= %ld/%ld\n", res.num, res.denom);
}

rational_t str_to_rational(char *chlen) {
    // Поиск первого вхождения строки "last" в строке chlen (http://all-ht.ru/inf/prog/c/func/strstr.html). 
    // Проверяем содержит ли строка chlen = last, если да, то возвращаем значение last иначе возвращаем числитель и знаменатель в формате rational_t
    // Переменная str в которую будет занесен адрес первой найденной строки 
    char *str = strstr("last", chlen);
    if (str!=NULL) {
        return last;
    }

    // Иначе выводим дробь 
    long num=0, denom=0;

    // sscanf - это scanf, но только данные получаются не из консоли, а из строки chlen. Символ дроби надо игнорировать
    sscanf(chlen, "%ld%*c%ld", &num, &denom);
    
    // Проверяем дробь на наличие отрицательных значений в числителе и знаменателе перед передачей в функцию rational(), где отрицательным числам не место (unsigned long)
    if (num < 0) {
    //    printf("numErator < 0= %ld\n", num);      // ОТЛАДКА 
	    num = num*(-1);
    }
    if (denom < 0) {
    //    printf("denominator < 0= %ld\n", denom); // ОТЛАДКА
	    denom = denom*(-1);
    }
    
    // Приводим числа 0 или 0/n к виду 0/1
    if (num == 0) {
	    num = 0;
	    denom = 1;
    }

    // Приводим числа n/0 к виду 0/0
    if (denom == 0) {
        num = 0;
	    denom = 0;
    }

    return rational(num, denom);
}
