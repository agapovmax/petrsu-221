// https://stepik.org/lesson/53161/step/9?unit=31258

/*
Поле для игры в рулетку состоит из ячеек от 0 до N.  На вход программе подаётся одно натуральное число N.
Программа должна выдать случайное число от нуля до N включительно.
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    int n;
    scanf("%d", &n);

    srand(time(NULL));
    printf("%d\n", 0 + rand()%(n+1));

    return 0;
}