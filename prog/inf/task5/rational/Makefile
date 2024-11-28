librational: rational.o rat_math.o rat_io.o librational.so

librational.so: rational.o rat_math.o rat_io.o
	gcc -shared -o librational.so rational.o rat_math.o rat_io.o

rational.o: rational.c rational.h
	gcc -g -fPIC -O0 -c rational.c

rat_math.o: rat_math.c rat_math.h
	gcc -g -fPIC -O0 -c rat_math.c

rat_io.o: rat_io.c rat_io.h
	gcc -g -fPIC -O0 -c rat_io.c

clean:
	rm -f *.o *.so