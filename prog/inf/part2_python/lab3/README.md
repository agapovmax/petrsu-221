### Тестирование при помощи pytest

1. Необходимо создать директорию с csv файлами, содержащие ошибки. Для которых мы собственно и будем запускать тесты.

ls pytests/

no_second_column.csv - отсутствует вторая колонка value во второй строке
incorrect_types.csv - некорректные типы данных в столбцах (символы, float)
 

# Код для добавления в main.py для корректного отрабатывания 4 теста с отсутствием колонок. Текущая проблема 

```
data = [(float(row[0]), int(row[1])) for row in raw_csv]  # Падает с IndexError если нет row[1]
```


# Измениим код
def read_data_from_file(filename):
    with open(filename, mode='r', newline='') as file:
        raw_csv = csv.reader(file)
        next(raw_csv)  # Пропускаем заголовок
        data = []
        for row_num, row in enumerate(raw_csv, start=2):  # start=2 учитывает заголовок
            if len(row) < 2:
                raise ValueError(f"Строка {row_num} содержит менее 2 колонок")
            try:
                data.append((float(row[0]), int(row[1])))
            except ValueError as e:
                raise ValueError(f"Ошибка в строке {row_num}: {str(e)}")
        return data



# Добавим в тест 
def test_missing_columns():
    with pytest.raises(ValueError) as exc_info:
        read_data_from_file("tests/test_data/missing_columns.csv")
    assert "Строка 3 содержит менее 2 колонок" in str(exc_info.value)
