import csv
import sys
from statistics import mean, mode, median
from data_splitter import split_data


# Чтение данных из csv-файла
def read_data_from_file(filename):
    with open(filename, mode='r', newline='') as file:
        raw_csv = csv.reader(file)
        # Пропустить первую строку
        next(raw_csv)
        # Чтение первого столбца (0) с временными метками (например 1.75390625) и второго столбца (1) с некоторыми значениеми (182)
        data = [(float(row[0]), int(row[1])) for row in raw_csv]
    return data

# Вывод статистики из отрезков
def calculate_statistics(data_chunks):
    # Проход по парам с индексом текущего отрезка и отрезком данных
    for i, chunk in enumerate(data_chunks):
        # zip нужен чтобы разделить каждый отрезок из пары (временная метка и значение) на два отдельных кортежа. Кортеж нужен, чтобы с ним корректно работал statistics 
        times, values = zip(*chunk)
        # Первая и последняя временные метки
        start_time = times[0]
        end_time = times[-1]

        # Количество значений с функцией len
        count = len(values)
        # Среднее значение с функцией mean
        avg = mean(values)
        # Проверка на типичность. Как часто повторялось значение с функцией mode
        try:
            mod = mode(values)
        except:
            mod = 'Нет моды'
        # Медианное значнение с функцией median
        med = median(values)

#        print(f"Отрезок {i+1} (от {start_time:.3f} до {end_time:.3f}):")
        print(f"Отрезок {i+1} (от {start_time} до {end_time}):")
        print(f"  Количество: {count}")
        print(f"  Среднее: {avg:.3f}")
        print(f"  Мода: {mod}")
        print(f"  Медиана: {med}\n")

# Запуск программы
if __name__ == "__main__":
    # Проверка аргументов (не меньше 3), так как имя программы тоже argv[0]
    if len(sys.argv) < 3:
        print("Использование: python3 main.py <путь_к_файлу.csv> <интервал>")
        sys.exit(1)
    
    # Путь до файла
    filename = sys.argv[1]
    # Интервал
    interval = float(sys.argv[2])

    # Работаем братья
    data = read_data_from_file(filename)
    data_chunks = split_data(data, interval)
    calculate_statistics(data_chunks)
