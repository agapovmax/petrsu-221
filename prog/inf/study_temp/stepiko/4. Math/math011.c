// https://stepik.org/lesson/41457/step/7?auth=login&unit=30905

// Написать программу, вычисляющую площадь треугольника по трём сторонам.


#include <stdio.h>
#include <math.h>

int main () {
    double a, b, c, p;
    scanf("%lf %lf %lf", &a, &b, &c);
    p = (a+b+c)/2;
    printf("%.2lf", sqrt(p*((p-a)*(p-b)*(p-c)) ));
}