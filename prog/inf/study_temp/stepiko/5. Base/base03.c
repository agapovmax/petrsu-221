// https://stepik.org/lesson/53872/step/4?auth=login&unit=32085

/*
Идёт k секунда суток. Определить, сколько целых часов и целых минут будут показывать электронные часы, если на 0-ой секунде они показывают 0 0.
*/

#include <stdio.h>
#include <math.h>

int s,h,m;

int main (void) {
    scanf("%d", &s);
    h = s /3600;
    m = (s - (h * 3600)) / 60;
    printf("%d %d", h, m );

    return 0;
}
