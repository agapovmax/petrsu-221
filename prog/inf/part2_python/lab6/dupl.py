#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import hashlib
from collections import defaultdict

def find_duplicates(root_dir):
    # Ищем дубликаты файлов в указанной директории и её поддиректориях
    files_by_size = defaultdict(list)
    files_by_hash = defaultdict(list)

    # Сначала группируем файлы по размеру (одинаковые файлы имеют одинаковый размер)
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                file_size = os.path.getsize(filepath)
                files_by_size[file_size].append(filepath)
            except (OSError, PermissionError):
                continue

    # Затем проверяем файлы с одинаковым размером по хешу
    for file_size, files in files_by_size.items():
        if len(files) > 1:
            for filepath in files:
                try:
                    file_hash = calculate_file_hash(filepath)
                    files_by_hash[file_hash].append(filepath)
                except (OSError, PermissionError):
                    continue

    # Возвращаем только те файлы, у которых есть дубликаты
    return [files for files in files_by_hash.values() if len(files) > 1]

def calculate_file_hash(filepath, block_size=65536):
    # Вычисляем хеш файлов
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hasher.update(block)
    return hasher.hexdigest()

def handle_duplicates(duplicates):
    # Обрабатываем найденные дубликаты, предлагая пользователю выбрать действие
    for i, duplicate_set in enumerate(duplicates, 1):
        print(f"\nНабор дубликатов #{i} ({len(duplicate_set)} файлов):")
        for j, filepath in enumerate(duplicate_set, 1):
            print(f"{j}: {filepath}")

        while True:
            choice = input(
                "\nВыберите действие:\n"
                f"1-{len(duplicate_set)}: Оставить файл с указанным номером, остальные удалить\n"
                "c: Оставить все файлы (пропустить этот набор)\n"
                "q: Выйти из программы\n"
                "Ваш выбор: "
            ).strip().lower()

            if choice == 'c':
                break
            elif choice == 'q':
                return False
            elif choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(duplicate_set):
                    keep_file = duplicate_set[index]
                    for filepath in duplicate_set:
                        if filepath != keep_file:
                            try:
                                os.remove(filepath)
                                print(f"Удалён: {filepath}")
                            except OSError as e:
                                print(f"Ошибка при удалении {filepath}: {e}")
                    break
                else:
                    print("Некорректный номер файла. Попробуйте снова.")
            else:
                print("Некорректный ввод. Попробуйте снова.")
    return True

def main():
    if len(sys.argv) != 2:
        print("Использование: python dupl.py <директория>")
        sys.exit(1)

    root_dir = sys.argv[1]
    if not os.path.isdir(root_dir):
        print(f"Ошибка: '{root_dir}' не является директорией или не существует.")
        sys.exit(1)

    print(f"Поиск дубликатов в директории: {root_dir}")
    duplicates = find_duplicates(root_dir)

    if not duplicates:
        print("Дубликаты не найдены.")
        return

    print(f"\nНайдено {len(duplicates)} наборов дубликатов.")
    handle_duplicates(duplicates)
    print("\nОбработка дубликатов завершена.")

if __name__ == "__main__":
    main()