calc: rational calc.o
	gcc -g -L./rational -lrational -o calc calc.o

calc.o:
	gcc -g -O0 -c calc.c

.PHONY: rational
rational:
	cd rational && $(MAKE)
	
clean:
	rm calc calc.o rational/*.o rational/*.so