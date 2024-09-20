# цель по умолчанию (при вызове make или make task1)
# собираем программу task1 из объектного файла task1.o
task1: main.o
	gcc -g -O0 -o task1 main.o

main.o: main.c
	gcc -g -O0 -c main.c

indent: main.c
	/usr/bin/indent -kr -nut main.c

# цель clean (при вызове make clean)
# удаляем программу и объектные файлы
clean:
	rm task1 *.o
