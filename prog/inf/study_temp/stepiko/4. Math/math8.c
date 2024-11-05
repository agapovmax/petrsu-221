// https://stepik.org/lesson/41090/step/6?auth=login&unit=30904

/*
Это решение не сработает, необходимо собирать исполняемый файл с параметром -lm чтобы появилась математичесикая функция 
*/
#include <stdio.h>
#include <math.h>

int main() {
    double x1, y1, x2, y2, resx, resy, res;
    scanf("%lf %lf %lf %lf", &x1, &y1, &x2, &y2);
    //printf("%.2lf", pow(((fabs(x2-x1))), 2) );
    resx = fabs(x2-x1);
    resy = fabs(y2-y1);

    resx = cpow(resx, 2);
    resy = cpow(resy, 2);
    res = sqrt(resx+resy);
    printf("%.2lf", res );
    return 0;
}