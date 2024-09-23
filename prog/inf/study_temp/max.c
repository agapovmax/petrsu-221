/* Вывод разных вариаций максимального значения LONG_MAX для проверки задания к третьей лабораторной работе*/
#include <stdio.h>
#include <limits.h>

int main()
{

	long max0 = LONG_MAX;
	long max1 = LONG_MAX - 1;	
	long max2 = (LONG_MAX - 1) / 10;
	long max3 = (LONG_MAX - 10) / 10;

	printf("Max: %ld, %ld, %ld, %ld\n", max0, max1, max2, max3);
	return 0;
}

