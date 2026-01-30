import pytest
import os, csv
from main import read_data_from_file, calculate_statistics
from data_splitter import split_data

# Тест 1: нет указанного файла
def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_data_from_file("data1.csv")

# Тест 2: файл не имеет прав на чтение
def test_permission_denied(tmp_path):
    file_path = tmp_path / "no_permission.csv"
    file_path.write_text("timestamp,value\n23.0,01230")
    os.chmod(file_path, 0o000)  # Убираем все права
    with pytest.raises(PermissionError):
        read_data_from_file(str(file_path))
    os.chmod(file_path, 0o644)  # Возвращаем права

# Тест 3: файл не формата csv. Чтобы правильно давал возврат, надо скорректировать функцию read_data_from_file для проверки расширения перед чтением
def test_invalid_format(tmp_path):
    txt_file = tmp_path / "data.txt"
    txt_file.write_text("1,2,3,abc")
    # with pytest.raises(csv.Error):
    #     read_data_from_file("pytests/keskus.jpg")
    with pytest.raises(ValueError, match="Файл должен иметь расширение .csv"):
        read_data_from_file(str(txt_file))

# Тест 4: в какой-то из строк файла только одна колонка. Похоже надо тоже править main.py для отлова верного исключения при чтении строк
def test_missing_columns():
    with pytest.raises(ValueError):
        read_data_from_file("pytests/no_second_column.csv")

# Тест 5: данные не заданного типа
def test_wrong_types():
    with pytest.raises(ValueError):
        read_data_from_file("pytests/incorrect_types.csv")

# Тест 6: Проверка корректного разделения на интервалы
def test_data_splitting():
#    data = read_data_from_file("data.csv")
    data = [(1.0, 100), (1.5, 200), (2.0, 150), (2.5, 300), (3.0, 250)]
    chunks = split_data(data, 1.0)
    assert len(chunks) == 3
    assert chunks[0] == [(1.0, 100), (1.5, 200)]
    assert chunks[1] == [(2.0, 150), (2.5, 300)]
    assert chunks[2] == [(3.0, 250)]

# Тест 7: Проверка статистики
def test_statistics_calculation(capsys):
    data = [(1.0, 100), (1.5, 200), (2.0, 150)]
    chunks = [data]
    calculate_statistics(chunks)
    captured = capsys.readouterr()
    assert "Количество: 3" in captured.out
    assert "Среднее: 150.000" in captured.out
    assert "Медиана: 150" in captured.out
#    assert "Мода: " in captured.out

# Тест 8: Проверка на пустой файл
def test_empty_file():
    with pytest.raises(StopIteration):
        read_data_from_file("pytests/empty_file.csv")

# Тест 9: Проверка на интервал больше общего времени
def test_large_interval():
    data = [(1.0, 100), (1.5, 200)]
    chunks = split_data(data, 10.0)
    assert len(chunks) == 1
    assert chunks[0] == data

# Тест 10: Проверка моды, когда нет повторяющихся значений
def test_no_mode(capsys):
    data = [(1.0, 100), (1.5, 200), (2.0, 150)]
    chunks = [data]
    calculate_statistics(chunks)
    captured = capsys.readouterr()
    assert "Мода: Нет моды" in captured.out
