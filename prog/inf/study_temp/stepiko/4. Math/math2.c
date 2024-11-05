// https://stepik.org/lesson/40857/step/6?auth=login&unit=30903

/*
На вход программы поступает натуральное трёхзначное число. Напишите программу, которая выводит сумму цифр этого числа.
*/

#include <stdio.h>

int main() {
    int a, res;
    scanf("%d %d %d", &a);
    res = (a % 100) + (a % 10 % 10) + (a % 10 % 10 % 10);
    printf("%d\n", a % 10); //третий десяток
    printf("%d\n", a % 100 / 10); // второй десяток
    printf("%d\n", a / 100);
    res = ((a % 10) + (a % 100 / 10) + (a / 100));
    printf("%d", res);
  return 0;
}