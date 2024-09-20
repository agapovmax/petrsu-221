/* Пример объявления переменной и область её действия*/

#include <stdio.h>

int a = 1;

int main () {
	int b = 2;
	{
		int c = 3;
		printf("%d\n", a);
		printf("%d\n", b);
		printf("%d\n", c);
	}
//	printf("%d\n", c);
}
