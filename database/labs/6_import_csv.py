import pyodbc
import pandas as pd
import os
import sys
from func import load_config, get_connection_string

def table_name_from_file(csv_path):
    """Получаем название таблицы из имени файла. Например: dbo.tblLesson.csv -> dbo.tblLesson"""
    return os.path.splitext(os.path.basename(csv_path))[0]


def get_date_columns(cursor, schema, table):
    """Возвращает список колонок с типами date"""
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
          AND DATA_TYPE IN ('date')
    """, schema, table)
    return [row[0] for row in cursor.fetchall()]


def table_exists(cursor, schema, table):
    cursor.execute("""
        SELECT 1 FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ? AND TABLE_TYPE = 'BASE TABLE'
    """, schema, table)
    return cursor.fetchone() is not None


def import_csv(csv_path, config):
    server   = config['connection']['server_name']
    database = config['connection']['database_name']
    login    = config['connection']['user_login']
    password = config['connection']['user_password']

    full_table = table_name_from_file(csv_path)
    schema, table = full_table.split('.', 1)

    print(f"CSV-файл:\t{csv_path}")
    print(f"Таблица:\t{full_table}")

    conn_str   = get_connection_string(server, database, login, password)
    connection = pyodbc.connect(conn_str)
    connection.autocommit = False
    cursor     = connection.cursor()

    if not table_exists(cursor, schema, table):
        print(f"Ошибка: таблица '{full_table}' не найдена в базе данных.")
        connection.close()
        sys.exit(1)

    # Читаем CSV, получаем количество строк
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig', dtype=str)
    print(f"Строк в файле:\t{len(df)}")

    # Конвертируем даты обратно в забугорский формат ISO (YYYY-MM-DD)
    date_cols = get_date_columns(cursor, schema, table)
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%d.%m.%Y', errors='coerce').dt.strftime('%Y-%m-%d')

    # Заменяем NaN на None (NULL в SQL)
    #df = df.where(pd.notna(df), None)

    # Определяем какие колонки являются IDENTITY чтобы для них отключить проверку FK, иначе будут ошибки
    cursor.execute(f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ? 
          AND COLUMNPROPERTY(OBJECT_ID(TABLE_NAME), COLUMN_NAME, 'IsIdentity') = 1
    """, (schema, table))
    
    identity_columns = [row[0] for row in cursor.fetchall()]
    
    # Если есть IDENTITY столбцы, временно разрешаем вставку
    if identity_columns:
        print(f"Найдены IDENTITY столбцы: {', '.join(identity_columns)}")
        print(f"Включаем IDENTITY_INSERT для таблицы {full_table}...")
        cursor.execute(f"SET IDENTITY_INSERT {full_table} ON")
    
    # Формируем список колонок для вставки (все колонки из CSV)
    columns = list(df.columns)
    col_list = ', '.join(f'[{c}]' for c in columns)
    placeholders = ', '.join(['?'] * len(columns))
    insert_sql = f"INSERT INTO {full_table} ({col_list}) VALUES ({placeholders})"

    try:
        # Отключаем проверку внешних ключей
        cursor.execute("EXEC sp_msforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT all'")
        
        # Очищаем таблицу
        cursor.execute(f"DELETE FROM {full_table}")
        deleted = cursor.rowcount
        print(f"Удалено строк: {deleted}")

        # Вставляем новые данные
        print("Вставляем данные из файла...")
        for idx, row in df.iterrows():
            cursor.execute(insert_sql, tuple(row))
            if (idx + 1) % 100 == 0:
                print(f"  Вставлено строк: {idx + 1}/{len(df)}")

        # Включаем проверку обратно
        print("Включаем обратно проверку внешних ключей...")
        cursor.execute("EXEC sp_msforeachtable 'ALTER TABLE ? CHECK CONSTRAINT all'")
        
        # Если включали IDENTITY_INSERT, выключаем его
        if identity_columns:
            cursor.execute(f"SET IDENTITY_INSERT {full_table} OFF")
            print(f"IDENTITY_INSERT выключен")
        
        connection.commit()
        print(f"Вставлено строк: {len(df)}")
        print("Импорт завершён успешно.")

    except pyodbc.Error as e:
        connection.rollback()
        print(f"Ошибка при импорте, изменения отменены: {e}")
        
        # Пытаемся выключить IDENTITY_INSERT при ошибке
        try:
            if identity_columns:
                cursor.execute(f"SET IDENTITY_INSERT {full_table} OFF")
        except:
            pass
            
        sys.exit(1)

    finally:
        connection.close()

def main():
    if len(sys.argv) != 2:
        print("Использование: python 6import_csv.py <путь_к_файлу.csv>")
        sys.exit(1)

    csv_path = sys.argv[1]

    if not os.path.isfile(csv_path):
        print(f"Ошибка: файл '{csv_path}' не найден.")
        sys.exit(1)

    config = load_config()
    import_csv(csv_path, config)


if __name__ == "__main__":
    main()
