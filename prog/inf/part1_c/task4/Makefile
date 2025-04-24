# Переменные для проекта

CC=/usr/bin/gcc
flags=-g -O0# -fsanitize=address - поможет в выводе исчерпывающей информации о сбое (SIGSEGV или SIGFPE)
#flags=-O0 # -fsanitize=address - поможет в выводе исчерпывающей информации о сбое (SIGSEGV или SIGFPE)
help=calculate_primes
prog=goldbach

# Цвета
CG=\033[0;32m # зеленый
CR=\033[0;31m # красный
CB=\033[0;34m # синий
CD=\033[0m    # стандартный

# Собрать все разом
#all: $(prog).c $(help).c
all: $(prog) primes
	
	@echo "INFO Start linking..."
	$(CC) $(flags) $(prog).o -o $(prog)
	@echo -e "INFO: Complete\n"

# Собрать main()
goldbach: goldbach.c primes
	
	@echo "INFO: Start compilation $(prog)"
	$(CC) $(flags) -c $(prog).c
	@echo -e "INFO: Complete\n"

# Собрать calculate_primes()
primes: calculate_primes.c
	
	@echo "INFO Start compilation $(help)"
	$(CC) $(flags) -c $(help).c
	@echo -e "INFO: Complete\n"

# Очистка файлов
clean:
	rm $(prog) 2>/dev/null
	rm  *.o 2>/dev/null