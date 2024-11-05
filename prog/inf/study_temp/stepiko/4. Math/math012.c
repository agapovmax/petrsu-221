// https://stepik.org/lesson/41457/step/8?auth=login&unit=30905

#include <stdio.h>
int main(void){

    double a, b, c, d, e, f, h, res;
    scanf("%lf %lf %lf %lf %lf %lf %lf", &a, &b, &c, &d, &e, &f, &h);
    res =  a / (b * (c / (d * (e / (f * h)))));
    printf("%.2lf", res);

  return 0;
}