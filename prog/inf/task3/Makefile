# Переменные для проекта

toolchain=/usr/bin/gcc
flags= -g -O0 -fsanitize=address # -fsanitize=address - поможет в выводе исчерпывающей информации о сбое (SIGSEGV или SIGFPE)
main=main.o
prog=lychrel

all: $(main)
	@echo "INFO Start linking..."
	$(toolchain) $(flags) -o $(prog) $(prog).o

$(main): $(prog)
	@echo "INFO Start compilation..."
	$(toolchain) $(flags) -c lychrel.c

# Очистка файлов
clean:
	rm  *.o


