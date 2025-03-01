// https://stepik.org/lesson/40857/step/7?auth=login&unit=30903

/* Составьте программу подсчёта размера оплаты за электроэнергию по показаниями счётчика и тарифу. На вход поступают 3 числа.
Первое число -- целое число. Показания счётчика в кВт*ч на начало месяца.
Второе число -- целое число. Показания счётчика в кВт*ч на конец месяца.
Третье число -- вещественное число. Стоимость одного кВт*ч в рублях.
Программа должны вывести на экран размер оплаты за электроэнергию. Результат выведите с двумя знаками после запятой.

Примечание: 
Здесь и далее до конца курса при необходимости использования вещественного типа переменной в задаче следует использовать тип double, а не float, для избежания ошибок округления.
*/

// самое важное в этом примере: использовать %lf для работы с типом double и квантификатор для вывода только двух десятичных чисел после точки в переменной res

#include <stdio.h>
int main() {
    int a,b;
    double w, res;
    
    scanf("%d%d%lf", &a, &b, &w);
    printf("%.2lf\n", res = (b - a) * w);
    // put your code here
    return 0;
}