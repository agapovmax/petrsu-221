import pyodbc
import pandas as pd
import os
from func import load_config, get_connection_string

def get_table_names(cursor):
    """
    Получаем список всех таблиц в текущей БД
    """
    query = """
    SELECT TABLE_SCHEMA + '.' + TABLE_NAME AS FullTableName -- точка нужна чтобы получить полное имя таблицы dbo.tblLesson
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE = 'BASE TABLE' 
        AND TABLE_NAME LIKE 'tbl%'  -- все не нужны, попадают какие-то служебные
        AND TABLE_NAME NOT LIKE '%[0-9]%' -- это после тестов с процедурами
    ORDER BY TABLE_SCHEMA, TABLE_NAME;
    """
    cursor.execute(query)
    tables = [row[0] for row in cursor.fetchall()]
    return tables

def export_table_to_csv(cursor, table_name, output_dir):
    """
    Выгружаем по одной таблице в CSV-файл
    """
    print(f"Выгрузка таблицы: {table_name}...")
    
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", cursor.connection)

    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col], format='%Y-%m-%d', errors='raise').dt.strftime('%d.%m.%Y')
        except (ValueError, TypeError):
            pass

    safe_name = table_name.replace('.', '_').replace('[', '').replace(']', '')
    file_path = os.path.join(output_dir, f"{table_name}.csv")
    df.to_csv(file_path, index=False, encoding='utf-8-sig', sep=';')

def main():
    config = load_config()

    server_name   = config['connection']['server_name']
    db_name       = config['connection']['database_name']
    user_login    = config['connection']['user_login']
    user_password = config['connection']['user_password']
    output_folder = config['output_folder']

    os.makedirs(output_folder, exist_ok=True)

    try:
        conn_str = get_connection_string(server_name, db_name, user_login, user_password)
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        print(f"Подключение к {db_name} успешно установлено")
        print("Получение списка таблиц...")
        
        tables = get_table_names(cursor)
        
        if not tables:
            print("В базе данных не найдено ни одной таблицы")
            return

        print(f"Найдено {len(tables)} таблиц. Начало выгрузки...")
        
        for tbl in tables:
            export_table_to_csv(cursor, tbl, output_folder)
        
        print("\nВыгрузка завершена успешно!")
        print(f"Файлы сохранены в папку: {output_folder}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    main()