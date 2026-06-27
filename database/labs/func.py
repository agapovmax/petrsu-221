import json

def load_config(config_path='config.json'):
    """
    Загружает настройки из JSON
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Ошибка: Файл {config_path} не найден")
        print("Создайте файл config.json с настройками подключения")
        exit(1)
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {config_path} содержит неверный формат")
        exit(1)

def get_connection_string(server, database, username, password):
    """
    Создание подключения к SQL
    """
    return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
