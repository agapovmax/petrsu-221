// https://stepik.org/lesson/41090/step/7?auth=login&unit=30904

/* 
Написать программу, вычисляющую площадь треугольника по двум сторонам и углу между ними.
*/

// Главной сложностью является дополнительный расчет синуса угла в радианах. Необходимо перевести градусы по формуле a * pi /180


#include <stdio.h>
#include <math.h>

const double pi = 3.141593;

int main () {
    double a, b, c;
    scanf("%lf %lf %lf", &a, &b, &c);
    // (a*b*sinc)/2
    printf("%.2lf", a*b*(sin(c*pi/180)) /2);

}