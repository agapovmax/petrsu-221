// https://stepik.org/lesson/40857/step/5?auth=login&unit=30903

/* На вход программы поступают два целых числа — длины сторон прямоугольника. Посчитайте и выведите периметр этого прямоугольника.

Периметр — сумма длин всех сторон.
*/

#include <stdio.h>

int main (void) {
    int a = 123, b =1000;
    int res;

    res = a + b;
    printf("%d + %d = %d\n", a, b, res);
    res = a - b;
    printf("%d - %d = %d\n", a, b, res);
    res = a*b;
    printf("%d * %d = %d\n", a, b, res);
    res = a / 100;
    printf("%d %% %d = %d\n", a, b, res);

    return 0;

}