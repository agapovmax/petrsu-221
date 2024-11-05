// https://stepik.org/lesson/53161/step/8?unit=31258

/*
Перепишите программу так, чтобы она выдавала случайно одно из чисел 0, 1 или 2.
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void){
    srand(time(NULL));
    int rand_digit = 0 + rand()%3;
    printf("%d\n",rand_digit);
    return 0;
}