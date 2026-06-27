-- Хранимая процедура: usp_CopyAllTables
-- Хорошим тоном является наименование usp (user stored procedure), сразу ясно что это ХП
-- Создаёт копии всех пользовательских таблиц с суффиксом в виде числового параметра @CopyNumber.
-- Пример: tblSubject -> tblSubject1
-- ПРимер запуска: EXEC dbo.usp_CopyAllTables @CopyNumber = 1;

-- CREATE OR ALTER: создаёт процедуру, если её нет, или заменяет существующую без DROP.
-- dbo.usp_CopyAllTables — полное имя: схема dbo, префикс usp = user stored procedure.
CREATE OR ALTER PROCEDURE dbo.usp_CopyAllTables         -- создаём процедуру если её нет, или заменяет существующую без DROP.
    @CopyNumber INT   -- входной параметр: число-суффикс, добавляемое к имени каждой копии (например, 1 чтобы получить как в примере tblSubject1)
-- для сравнения с классикой функции в ЯП
-- function copyAllTables(copyNumber) {
--    // тело функции
--}

AS -- начало тела ХП объявляется с этого оператора
BEGIN
    SET NOCOUNT ON;   -- отключает сообщения "N row(s) affected" после каждого DML-оператора, чтобы не засорять вывод

    -- Блок валидации входного параметра
    IF @CopyNumber IS NULL OR @CopyNumber < 0   -- NULL недопустим (потерянный параметр); отрицательное число даст некорректное имя таблицы
    BEGIN
        -- RAISERROR: аналог throw в ЯП. Генерирует ошибку с severity 16 (пользовательская ошибка, выполнение продолжается если нет TRY/CATCH), state 1
        RAISERROR(N'Параметр @CopyNumber должен быть неотрицательным целым числом.', 16, 1);
        RETURN;   -- немедленный выход из процедуры, дальнейший код не выполняется
    END;

    -- Объявление переменных
    DECLARE @SchemaName  NVARCHAR(4);       -- имя схемы текущей таблицы (например, 'dbo'); 128 — максимальная длина имени объекта в SQL Server
    DECLARE @TableName   NVARCHAR(64);      -- имя исходной таблицы (например, 'tblSubject')
    DECLARE @NewName     NVARCHAR(64);      -- имя будущей копии = @TableName + @Suffix (например, 'tblSubject1')
    DECLARE @SQL         NVARCHAR(MAX);   -- строка динамического SQL, которую будем собирать и исполнять
    DECLARE @Suffix      NVARCHAR(20);    -- строковое представление @CopyNumber (нужно для конкатенации строк)
    DECLARE @TableCount  INT;             -- счётчик таблиц для информационного вывода в консоль чтобы смотреть прогресс

    SET @Suffix = CAST(@CopyNumber AS NVARCHAR(20));   -- преобразуем число в строку: 1 -> '1', 42 -> '42'

    -- Временная таблица со снимком исходных таблиц. Очень важно её делать, так как всё может резко поменяться и кто-то создаст и запишет в новую таблицу
    CREATE TABLE #SourceTables   -- спецсимвол # означает локальную временную таблицу: видна только в текущей сессии
    (
        SchemaName NVARCHAR(128) NOT NULL,   -- схема таблицы
        TableName  NVARCHAR(128) NOT NULL    -- имя таблицы
    );

    -- Заполняем снимок из системного представления INFORMATION_SCHEMA.TABLES
    INSERT INTO #SourceTables (SchemaName, TableName)
    SELECT TABLE_SCHEMA, TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE = 'BASE TABLE'            -- только реальные таблицы, исключаем представления (VIEW)
      AND TABLE_NAME LIKE N'tbl%'              -- только таблицы с префиксом tbl (я так создавал таблицы из лабы, видишь, пригодилось чтобы не городить фильтры)
      AND TABLE_NAME NOT LIKE N'%[0-9]%'       -- исключаем уже существующие копии (tblSubject1, tblSubject2 и т.д.), чтобы не копировать копии
    ORDER BY TABLE_NAME;                       -- сортировка для предсказуемого порядка обработки

    SELECT @TableCount = COUNT(*) FROM #SourceTables;   -- запоминаем количество найденных таблиц для информационного сообщения

    -- Вывод в консоль
    PRINT N'=== Начало копирования (суффикс: ' + @Suffix + N') ===';
    PRINT N'Таблиц к копированию: ' + CAST(@TableCount AS NVARCHAR(10));   -- CAST нужен: PRINT не принимает INT напрямую

    -- Объявление курсора (курсор это механизм для построчного перебора таблиц.) 
    -- зачем LOCAL? Курсор виден только внутри этой процедуры, не «утекает» наружу. Есть ещё GLOBAL. Если будем использовать в других ХП - задачем ГЛОБАЛ
    -- зачем FAST_FORWARD? Оптимизированный курсор только для чтения вперёд (самый быстрый тип). А вообще есть другие виды курсоров:
            -- STATIC делает копию данных всей базы в момент объявлени. РЕсурсоёмкий для больших БД
            -- DYNAMIC самый меделенный - отслеживает изменение БД при перемещении курсора
            -- KEYSET видит изменения существующих, но новых не видит
            -- FAST_FORWARD как FAST, только можно менять
    DECLARE cur CURSOR LOCAL FAST_FORWARD FOR
        SELECT SchemaName, TableName FROM #SourceTables ORDER BY TableName;

    OPEN cur;                                              -- открываем курсор: SQL Server выполняет запрос и готовит набор строк
    FETCH NEXT FROM cur INTO @SchemaName, @TableName;      -- читаем первую строку в переменные; если строк нет — @@FETCH_STATUS сразу станет -1

    -- Основной цикл
    -- @@FETCH_STATUS = 0 успешное чтение строки; -1 = строк больше нет; -2 = строка была удалена
    WHILE @@FETCH_STATUS = 0
    BEGIN
        SET @NewName = @TableName + @Suffix;   -- строим имя копии: 'tblSubject' + '1' = 'tblSubject1'

        -- Удаление старой копии, если она уже существует
        -- OBJECT_ID проверяет существование объекта; 'U' = Пользовательская таблица (User table)
        -- QUOTENAME оборачивает имя в квадратные скобки: dbo -> [dbo], защита от SQL-инъекции через имена
        -- Функция OBJECT_ID() ожидает на вход параметр типа NVARCHAR (или NCHAR), а не обычный VARCHAR.
        -- Без N будет передан VARCHAR(125) (однобайтовая кодировка, ANSI/CP1251)
        -- С N будет NVARCHAR(125) (Unicode, двухбайтовая кодировка UTF-16)
        -- важно если есть русские символы в наименовании таблиц bdo.ТАблицаБанк
        -- Это нечто! Если не указать явно N'.', то точка может преобразовать все имя из NVARCHAR в VARCHAR!!! Жесть
        IF OBJECT_ID(QUOTENAME(@SchemaName) + N'.' + QUOTENAME(@NewName), 'U') IS NOT NULL
        BEGIN
            -- Собираем строку DROP TABLE динамически, ибо имена таблиц нельзя передать параметром в sp_executesql
            SET @SQL = N'DROP TABLE '
                     + QUOTENAME(@SchemaName) + N'.'   -- например: [dbo].
                     + QUOTENAME(@NewName);             -- например: [tblSubject1]
            EXEC sp_executesql @SQL;                   -- выполняем динамический SQL; sp_executesql безопаснее EXEC(@SQL)
            PRINT N'  Удалена существующая копия: '
                + @SchemaName + N'.' + @NewName;       -- логируем факт удаления
        END;

        -- Создание копии таблицы
        -- SELECT * INTO создаёт новую таблицу и копирует в неё все строки за одну операцию
        -- Копируются: структура колонок + данные
        -- НЕ копируются: индексы, PK/FK/CHECK-ограничения, триггеры, права доступа.
        SET @SQL = N'SELECT * INTO '
                 + QUOTENAME(@SchemaName) + N'.' + QUOTENAME(@NewName)    -- цель: [dbo].[tblSubject1]
                 + N' FROM '
                 + QUOTENAME(@SchemaName) + N'.' + QUOTENAME(@TableName); -- источник: [dbo].[tblSubject]
        EXEC sp_executesql @SQL;   -- выполняем — таблица-копия создана и заполнена

        -- Логируем успешное копирование
        -- получим что-то вроде "Скопировано: [dbo].[tblSubject] -> [dbo].[tblSubject1]"
        PRINT N'  Скопировано: '
            + QUOTENAME(@SchemaName) + N'.' + QUOTENAME(@TableName)   -- источник
            + N' -> '
            + QUOTENAME(@SchemaName) + N'.' + QUOTENAME(@NewName);    -- куда скопировано

        FETCH NEXT FROM cur INTO @SchemaName, @TableName;   -- переходим к следующей строке курсора
    END;

    -- Завершение и очистка
    CLOSE cur;             -- закрываем курсор: освобождает текущий набор строк, но объект курсора ещё существует
    DEALLOCATE cur;        -- уничтожаем объект курсора и освобождает все связанные ресурсы памяти
    DROP TABLE #SourceTables;   -- явно удаляем временную таблицу (она и так удалится при закрытии сессии, но явная очистка — хороший тон)

    PRINT N'=== Копирование завершено ===';   -- финальное сообщение об успешном окончании
END;
GO   -- GO — разделитель пакетов (batch separator) в SSMS/sqlcmd; сигнализирует клиенту отправить всё до этой точки на сервер как один пакет

-- Пример вызова
-- EXEC dbo.usp_CopyAllTables @CopyNumber = 1;
