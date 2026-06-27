-- Триггер: по одному предмету нельзя провести два урока в один день.
-- Логика: при INSERT или UPDATE проверяем, нет ли уже урока с такой же парой (intSubjectId + darLessonDate) в таблице.
-- Если есть — откатываем транзакцию и бросаем ошибку.

-- Срабатывает после того, как строка уже добавлена в таблицу.
-- Если нашли дубль — откатываемся, строка исчезнет.
CREATE OR ALTER TRIGGER dbo.trg_tblLesson_NoDuplicateDay_Insert
ON dbo.tblLesson
AFTER INSERT    -- срабатывает на INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- inserted — виртуальная таблица в которой лежит сам запрос на INSERT. НАпример intSubjectId=1, darLessonDate='2026-05-25'
    -- Ищем в tblLesson урок с той же датой и тем же предметом,
    -- но с другим intLessonId (т.е. не саму только что вставленную строку).
    IF EXISTS (     -- надо сверить, что вставляемая строка из виртуальной таблицы совпадает с той что уже есть в tblLesson.
        SELECT 1
        FROM   dbo.tblLesson AS l
        JOIN   inserted      AS i
               ON  l.intSubjectId  = i.intSubjectId
               AND l.darLessonDate = i.darLessonDate
               AND l.intLessonId  <> i.intLessonId   -- !!!исключаем саму вставленную строку
    )
    BEGIN
        ROLLBACK TRANSACTION;   -- отменяем весь INSERT
        RAISERROR(N'Ошибка: по этому предмету уже есть урок в этот день. Два урока в один день — перебор.', 16, 1); --16 (пользовательская ошибка), 1 - состояние ошибки. Сам задаю
    END;
END;
GO

-- Тот же смысл, но при изменении даты или предмета урока. Вдруг кто-то решит перенести урок на день, где уже есть занятие.
CREATE OR ALTER TRIGGER dbo.trg_tblLesson_NoDuplicateDay_Update
ON dbo.tblLesson
AFTER UPDATE -- срабатывает на UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    
    IF UPDATE(darLessonDate) OR UPDATE(intSubjectId) -- проверяем только если изменились столбцы, которые влияют на уникальность
    BEGIN
        IF EXISTS (
            SELECT 1
            FROM   dbo.tblLesson AS l
            JOIN   inserted      AS i
                   ON  l.intSubjectId  = i.intSubjectId
                   AND l.darLessonDate = i.darLessonDate
                   AND l.intLessonId  <> i.intLessonId
        )
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR(N'Ошибка: по этому предмету уже есть урок в этот день. Перенос невозможен.', 16, 1);
        END;
    END;
END;
GO


-- ============================================================
-- ПРОВЕРКА
-- ============================================================

DECLARE @SubjectId INT = 9;  -- проверяем на предмете 9 (Информатика)

PRINT N'Текущие уроки предмета ' + CAST(@SubjectId AS VARCHAR) + N':';
SELECT intLessonId AS [ID урока], darLessonDate AS [Дата], txtTheme AS [Тема]
FROM   dbo.tblLesson
WHERE  intSubjectId = @SubjectId
ORDER BY darLessonDate;


-- ── Тест 1: вставка дубля по дате ─────────────────────────
-- Берём дату уже существующего урока и пытаемся добавить ещё один.
-- Ожидание: триггер откатит INSERT и покажет ошибку.
PRINT N'';
PRINT N'Тест 1: INSERT с дублирующей датой — должна быть ошибка';

DECLARE @ExistingDate DATE = (
    SELECT TOP 1 darLessonDate FROM dbo.tblLesson
    WHERE intSubjectId = @SubjectId
    ORDER BY darLessonDate
);
PRINT N'Пытаемся добавить урок на дату: ' + CAST(@ExistingDate AS VARCHAR);

BEGIN TRY
    INSERT INTO dbo.tblLesson (intSubjectId, darLessonDate, txtTheme)
    VALUES (@SubjectId, @ExistingDate, N'Дубль — не должен вставиться');

    PRINT N'Тест 1 ПРОВАЛЕН: строка вставилась, а не должна была';
END TRY
BEGIN CATCH
    PRINT N'Тест 1 ПРОЙДЕН: триггер поймал дубль. Ошибка: ' + ERROR_MESSAGE();
END CATCH;


-- ── Тест 2: вставка нормального урока ─────────────────────
-- Дата, которой точно нет — должно пройти без ошибок.
PRINT N'';
PRINT N'Тест 2: INSERT с новой датой — должен пройти';

BEGIN TRY
    INSERT INTO dbo.tblLesson (intSubjectId, darLessonDate, txtTheme)
    VALUES (@SubjectId, '2099-12-31', N'Урок из будущего — тест триггера');

    PRINT N'Тест 2 ПРОЙДЕН: урок добавлен';
END TRY
BEGIN CATCH
    PRINT N'Тест 2 ПРОВАЛЕН. Ошибка: ' + ERROR_MESSAGE();
END CATCH;


-- ── Тест 3: UPDATE — перенос на занятую дату ──────────────
-- Берём только что добавленный урок и пытаемся сдвинуть его
-- на дату, где уже есть другой урок этого предмета.
-- Ожидание: триггер откатит UPDATE.
PRINT N'';
PRINT N'Тест 3: UPDATE darLessonDate на занятую дату — должна быть ошибка';

DECLARE @NewLessonId INT = (SELECT MAX(intLessonId) FROM dbo.tblLesson WHERE intSubjectId = @SubjectId);

BEGIN TRY
    UPDATE dbo.tblLesson
    SET    darLessonDate = @ExistingDate  -- занятая дата из Теста 1
    WHERE  intLessonId   = @NewLessonId;

    PRINT N'Тест 3 ПРОВАЛЕН: UPDATE прошёл, а не должен был';
END TRY
BEGIN CATCH
    PRINT N'Тест 3 ПРОЙДЕН: триггер заблокировал перенос. Ошибка: ' + ERROR_MESSAGE();
END CATCH;


-- ── Уборка: удаляем тестовый урок из Теста 2 ──────────────
DELETE FROM dbo.tblLesson WHERE intLessonId = @NewLessonId;
PRINT N'';
PRINT N'Тестовый урок удалён. Финальное состояние предмета ' + CAST(@SubjectId AS VARCHAR) + N':';

SELECT intLessonId AS [ID], darLessonDate AS [Дата], txtTheme AS [Тема]
FROM   dbo.tblLesson
WHERE  intSubjectId = @SubjectId
ORDER BY darLessonDate;
