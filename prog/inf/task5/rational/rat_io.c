#include <stdio.h>
#include <string.h>
#include "rat_io.h"
#include "rat_math.h"
#include "rational.h"

// Переменная для последнего введенного значения в виде дроби
rational_t last;

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
    printf("Первая дробь %ld\t\tВторая дробь %ld\n", ch1, ch2);
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
    printf("Результат= %ld\t\t\t%ld\n", res.num, res.denom);
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
    printf("После перевода из строки = %ld\t\t%ld\n", num, denom);
    return rational(num, denom);
}