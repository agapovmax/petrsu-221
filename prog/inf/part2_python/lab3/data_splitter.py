# Разбивка данных data на отрезки data_chunks по интервалам interval
def split_data(data, interval):
    # Список для хранения всех отрезков 
    data_chunks = []
    # Список для хранения текущего отрезка
    current_chunk = [] 

    for point in data:
        # Каждый point как кортеж из временной метки и значения
        time, value = point
        # Добавление point в текущий отрезок если current_chunk пуст либо разница между текущим временем (time) и временем первой точки в current_chunk меньше interval, то текущая точка добавляется в current_chunk
        if not current_chunk or (time - current_chunk[0][0]) < interval:
            current_chunk.append(point)
        # Если текущее время не подходит под условие добавления в current_chunk, значит текущий отрезок завершен. current_chunk добавляется в data_chunks и начинается новый отрезок с текущей точки
        else:
            data_chunks.append(current_chunk)
            current_chunk = [point]

    # Проверка если current_chunk не пуст, то он добавляется в data_chunks, чтобы учесть последний отрезок данных, остаток
    if current_chunk:
        data_chunks.append(current_chunk)

    return data_chunks
