calc: rational calc.o
	gcc -g -L./rational -lrational -o calc calc.o

calc.o:
	gcc -g -O0 -c calc.c

.PHONY: rational
rational:
# https://www.gnu.org/software/make/manual/html_node/MAKE-Variable.html
	cd rational && $(MAKE) 

clean:
	rm calc calc.o rational/*.o rational/*.so 2>/dev/null

clear:
	rm calc calc.o rational/*.o rational/*.so 2>/dev/null