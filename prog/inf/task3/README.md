# Работа с отладчиком

## 1. Открыв программу в отладчике, поставьте контрольную точку на строку вызова функции проверки числа if (is_lychrel_candidate(number)) {. 

Установить точку останова можно по номеру строки в исходнике, либо по имени функции. В данном случае, функция будет называться **show_lychrel_candidates**

```c
break show_lychrel_candidates
Breakpoint 1 at 0x4005c3: file lychrel.c, line 33.
```

Но на самом деле, точка будет установлена на 33 строку с кодом

```c
for (number = 1; number <= last_number; number++) {
```

Можно установить конкретный номер искомой в вопросе строки 35
```c
break 35 
Breakpoint 1 at 0x4005cd: file lychrel.c, line 35.
```

## 2. Запустите программу, введите в качестве верхней границы 200. Остановившись в контрольной точке, подмените средствами отладчика значение переменной number сразу на 196. 
Выполним run
```bash
run
Starting program: /home/01/mtagapov/inf/task3/lychrel
Введите верхнюю границу отрезка поиска чисел Лишрел: 200

Breakpoint 1, show_lychrel_candidates (last_number=200) at lychrel.c:33
33          for (number = 1; number <= last_number; number++) {
```

## 2.1 Остановившись в контрольной точке, подмените средствами отладчика значение переменной number сразу на 196. Так?
```bash
set var number=196
```
