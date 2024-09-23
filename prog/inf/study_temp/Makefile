all: scope.o size.o max.o
	gcc -g -O0 -o scope scope.o
	gcc -g -O0 -o size size.o
	gcc -g -O0 -o max max.o

scope: scope.o
	gcc -g -O0 -o scope scope.o

scope.o: scope.c
	gcc -g -O0 -c scope.c

size: size.o
	gcc -g -O0 -o size size.o

size.o: size.c
	gcc -g -O0 -c size.c

max: max.o
	gcc -g -O0 -o max max.o

max.o: max.c
	gcc -g -O0 -c max.c

clean:
	rm scope
	rm size
	rm max
	rm *.o
