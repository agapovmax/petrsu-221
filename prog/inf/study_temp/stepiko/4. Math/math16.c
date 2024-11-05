// https://stepik.org/lesson/53161/step/10?unit=31258

/*
На вход программе подаётся два числа S и E, записанных через пробел. При этом гарантируется, что S≤E. 
Программа должна выводить одно случайное число из промежутка [S;E]
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main (void) {
    int a, b;
    srand(time(NULL));

    scanf("%d %d", &a, &b);
    printf("%d", a + rand()%(b-a+1));

    return 0;
}