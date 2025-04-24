/**
 * "floor.c -- программа для расчета нужного этажа"
 *
 * Copyright (c) 2024, Max Agapov <mtagapov@cs.petrsu.ru>
 *
 * This code is licensed under MIT license.
 */

#include "/usr/include/stdio.h"

int main()
{
    /* Номер квартиры, Число квартир на этаже */
    int flat_number, flats_per_floor;

    /* Запрашиваем квартиру, в которой проживает адресат */
    printf("Введите номер интересующей квартиры: ");
    scanf("%d", &flat_number);
    while(flat_number <= 0) {
	   printf("Введи верное значение больше 0: ");
	   scanf("%d", &flat_number);
	}

    /* Запрашиваем число квартир на этаже */
    printf("Введите число квартир на каждом этаже: ");
    scanf("%d", &flats_per_floor);
    while(flat_number <= 0) {
	   printf("Введи верное значение больше 0: ");
	   scanf("%d", &flat_number);
	}

    /* Рассчитываем и выводим номер этажа */
    int floor = ((flat_number - 1) / flats_per_floor) + 1;
    printf("Вам нужно подняться на %d этаж\n",
           floor);

    return 0;
}
