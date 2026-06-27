-- ============================================================
-- Файл: 10triggers_lesson_count.sql
-- Триггеры для поддержания целостности intLessonCount в tblSubject.
-- Счётчик уроков обновляется автоматически при любом изменении tblLesson.
-- ============================================================


-- ============================================================
-- ЧАСТЬ 1. ТРИГГЕРЫ
-- ============================================================

-- ── Триггер 1 ──────────────────────────────────────────────
-- trg_tblLesson_AfterInsert
-- Срабатывает после INSERT в tblLesson.
-- Увеличивает intLessonCount затронутых предметов.
CREATE OR ALTER TRIGGER dbo.trg_tblLesson_AfterInsert
ON dbo.tblLesson
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- inserted — псевдотаблица со вставленными строками (может быть несколько при массовом INSERT)
    UPDATE s
    SET    s.intLessonCount = ISNULL(s.intLessonCount, 0) + cnt.added
    FROM   dbo.tblSubject AS s
    JOIN (
        SELECT intSubjectId, COUNT(*) AS added
        FROM   inserted
        GROUP  BY intSubjectId
    ) AS cnt ON s.intSubjectId = cnt.intSubjectId;
END;
GO


-- ── Триггер 2 ──────────────────────────────────────────────
-- trg_tblLesson_AfterDelete
-- Срабатывает после DELETE из tblLesson.
-- Уменьшает intLessonCount затронутых предметов.
CREATE OR ALTER TRIGGER dbo.trg_tblLesson_AfterDelete
ON dbo.tblLesson
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- deleted — псевдотаблица с удалёнными строками
    UPDATE s
    SET    s.intLessonCount = ISNULL(s.intLessonCount, 0) - cnt.removed
    FROM   dbo.tblSubject AS s
    JOIN (
        SELECT intSubjectId, COUNT(*) AS removed
        FROM   deleted
        GROUP  BY intSubjectId
    ) AS cnt ON s.intSubjectId = cnt.intSubjectId;
END;
GO


-- ── Триггер 3 ──────────────────────────────────────────────
-- trg_tblLesson_AfterUpdate
-- Срабатывает при UPDATE строки в tblLesson.
-- Если изменился intSubjectId (урок переносится к другому предмету):
--   уменьшает счётчик старого предмета и увеличивает новому.
CREATE OR ALTER TRIGGER dbo.trg_tblLesson_AfterUpdate
ON dbo.tblLesson
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- UPDATE(col) = TRUE только если столбец был указан в SET-части запроса
    IF UPDATE(intSubjectId)
    BEGIN
        -- Уменьшаем счётчик предмета-источника (откуда ушёл урок)
        UPDATE s
        SET    s.intLessonCount = ISNULL(s.intLessonCount, 0) - cnt.removed
        FROM   dbo.tblSubject AS s
        JOIN (
            SELECT d.intSubjectId, COUNT(*) AS removed
            FROM   deleted  AS d
            JOIN   inserted AS i ON d.intLessonId = i.intLessonId
            WHERE  d.intSubjectId <> i.intSubjectId   -- только строки, где предмет реально сменился
            GROUP  BY d.intSubjectId
        ) AS cnt ON s.intSubjectId = cnt.intSubjectId;

        -- Увеличиваем счётчик предмета-получателя (куда пришёл урок)
        UPDATE s
        SET    s.intLessonCount = ISNULL(s.intLessonCount, 0) + cnt.added
        FROM   dbo.tblSubject AS s
        JOIN (
            SELECT i.intSubjectId, COUNT(*) AS added
            FROM   inserted AS i
            JOIN   deleted  AS d ON i.intLessonId = d.intLessonId
            WHERE  d.intSubjectId <> i.intSubjectId
            GROUP  BY i.intSubjectId
        ) AS cnt ON s.intSubjectId = cnt.intSubjectId;
    END;
END;
GO


-- ── Триггер 4 ──────────────────────────────────────────────
-- trg_tblSubject_ValidateLessonCount
-- Защита от прямого изменения intLessonCount вручную.
-- Если после UPDATE значение не совпадает с реальным подсчётом —
-- автоматически исправляет его по данным tblLesson.
--
-- Почему нет бесконечной рекурсии:
--   SQL Server по умолчанию отключает RECURSIVE_TRIGGERS,
--   поэтому внутренний UPDATE внутри триггера не запустит этот же триггер повторно.
CREATE OR ALTER TRIGGER dbo.trg_tblSubject_ValidateLessonCount
ON dbo.tblSubject
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(intLessonCount)
    BEGIN
        -- Пересчитываем только те строки, где значение оказалось неверным
        UPDATE s
        SET    s.intLessonCount = ISNULL(actual.cnt, 0)
        FROM   dbo.tblSubject AS s
        JOIN   inserted AS i ON s.intSubjectId = i.intSubjectId
        LEFT JOIN (
            SELECT intSubjectId, COUNT(*) AS cnt
            FROM   dbo.tblLesson
            GROUP  BY intSubjectId
        ) AS actual ON s.intSubjectId = actual.intSubjectId
        WHERE  s.intLessonCount <> ISNULL(actual.cnt, 0);
    END;
END;
GO


-- ============================================================
-- ЧАСТЬ 2. ПРОВЕРКА ТРИГГЕРОВ
-- ============================================================

-- Перед тестами INSERT можно уточнить структуру tblLesson:
-- EXEC sp_help 'dbo.tblLesson';


-- ── 0. Исходное состояние ─────────────────────────────────
PRINT N'=== 0. Исходное состояние ===';
SELECT
    s.intSubjectId       AS [ID],
    s.intSubjectName     AS [Предмет],
    s.intLessonCount     AS [intLessonCount],
    COUNT(l.intLessonId) AS [Факт. уроков],
    CASE
        WHEN s.intLessonCount = COUNT(l.intLessonId) THEN N'OK'
        ELSE N'РАСХОЖДЕНИЕ — запустите usp_RefreshLessonCount'
    END                  AS [Статус]
FROM  dbo.tblSubject AS s
LEFT  JOIN dbo.tblLesson AS l ON s.intSubjectId = l.intSubjectId
GROUP BY s.intSubjectId, s.intSubjectName, s.intLessonCount
ORDER BY s.intSubjectId;


-- ── Тест 1: INSERT-триггер ────────────────────────────────
-- Добавляем новый урок к предмету 1.
-- Ожидание: intLessonCount предмета 1 увеличится на 1.
PRINT N'';
PRINT N'=== Тест 1: INSERT (добавление урока к предмету 1) ===';

DECLARE @t1_before INT = (SELECT intLessonCount FROM dbo.tblSubject WHERE intSubjectId = 1);
PRINT N'intLessonCount предмета 1 ДО INSERT: ' + CAST(@t1_before AS NVARCHAR(10));

-- Вставьте тестовый урок, подставив реальные имена столбцов вашей таблицы:
-- Пример (скорректируйте имена/типы столбцов под вашу схему):
INSERT INTO dbo.tblLesson (intSubjectId, dtLessonDate, strLessonTopic)
VALUES                    (1,            '2026-05-18',  N'Тест триггера — тема');

DECLARE @t1_after  INT = (SELECT intLessonCount FROM dbo.tblSubject WHERE intSubjectId = 1);
PRINT N'intLessonCount предмета 1 ПОСЛЕ INSERT: ' + CAST(@t1_after AS NVARCHAR(10));
PRINT CASE
    WHEN @t1_after = @t1_before + 1
    THEN N'Тест 1 ПРОЙДЕН: счётчик увеличился на 1'
    ELSE N'Тест 1 ПРОВАЛЕН: ожидалось '
         + CAST(@t1_before + 1 AS NVARCHAR(10)) + N', получено ' + CAST(@t1_after AS NVARCHAR(10))
END;


-- ── Тест 2: DELETE-триггер ────────────────────────────────
-- Удаляем тестовый урок, добавленный в Тесте 1.
-- Ожидание: intLessonCount предмета 1 уменьшится на 1.
PRINT N'';
PRINT N'=== Тест 2: DELETE (удаление тестового урока предмета 1) ===';

DECLARE @t2_before INT = (SELECT intLessonCount FROM dbo.tblSubject WHERE intSubjectId = 1);
PRINT N'intLessonCount предмета 1 ДО DELETE: ' + CAST(@t2_before AS NVARCHAR(10));

-- Удаляем последний добавленный урок предмета 1 (тестовый из Теста 1)
DELETE FROM dbo.tblLesson
WHERE  intLessonId = (SELECT MAX(intLessonId) FROM dbo.tblLesson WHERE intSubjectId = 1);

DECLARE @t2_after INT = (SELECT intLessonCount FROM dbo.tblSubject WHERE intSubjectId = 1);
PRINT N'intLessonCount предмета 1 ПОСЛЕ DELETE: ' + CAST(@t2_after AS NVARCHAR(10));
PRINT CASE
    WHEN @t2_after = @t2_before - 1
    THEN N'Тест 2 ПРОЙДЕН: счётчик уменьшился на 1'
    ELSE N'Тест 2 ПРОВАЛЕН: ожидалось '
         + CAST(@t2_before - 1 AS NVARCHAR(10)) + N', получено ' + CAST(@t2_after AS NVARCHAR(10))
END;


-- ── Тест 3: UPDATE-триггер ────────────────────────────────
-- Переносим последний урок предмета 1 → предмет 2.
-- Ожидание: счётчик предмета 1 уменьшится на 1, предмета 2 увеличится на 1.
PRINT N'';
PRINT N'=== Тест 3: UPDATE intSubjectId (перенос урока из предмета 1 в предмет 2) ===';

DECLARE @t3_before1 INT = (SELECT intLessonCount FROM dbo.tblSubject WHERE intSubjectId = 1);
DECLARE @t3_before2 INT = (SELECT intLessonCount FROM dbo.tblSubject WHERE intSubjectId = 2);
PRINT N'Предмет 1 ДО: ' + CAST(@t3_before1 AS NVARCHAR(10))
    + N'  |  Предмет 2 ДО: '  + CAST(@t3_before2 AS NVARCHAR(10));

DECLARE @MovedId INT = (SELECT MAX(intLessonId) FROM dbo.tblLesson WHERE intSubjectId = 1);
UPDATE dbo.tblLesson SET intSubjectId = 2 WHERE intLessonId = @MovedId;

DECLARE @t3_after1 INT = (SELECT intLessonCount FROM dbo.tblSubject WHERE intSubjectId = 1);
DECLARE @t3_after2 INT = (SELECT intLessonCount FROM dbo.tblSubject WHERE intSubjectId = 2);
PRINT N'Предмет 1 ПОСЛЕ: ' + CAST(@t3_after1 AS NVARCHAR(10))
    + N'  |  Предмет 2 ПОСЛЕ: ' + CAST(@t3_after2 AS NVARCHAR(10));
PRINT CASE
    WHEN @t3_after1 = @t3_before1 - 1 AND @t3_after2 = @t3_before2 + 1
    THEN N'Тест 3 ПРОЙДЕН: оба счётчика обновлены корректно'
    ELSE N'Тест 3 ПРОВАЛЕН'
END;

-- Восстанавливаем урок обратно в предмет 1
UPDATE dbo.tblLesson SET intSubjectId = 1 WHERE intLessonId = @MovedId;
PRINT N'Урок ' + CAST(@MovedId AS NVARCHAR(10)) + N' возвращён в предмет 1 (восстановление данных)';


-- ── Тест 4: Защитный триггер tblSubject ──────────────────
-- Вручную ставим заведомо неверное значение intLessonCount = -999.
-- Ожидание: триггер автоматически исправит значение на реальное количество уроков.
PRINT N'';
PRINT N'=== Тест 4: Защита от ручной порчи intLessonCount ===';

DECLARE @t4_real INT = (SELECT COUNT(*) FROM dbo.tblLesson WHERE intSubjectId = 1);
PRINT N'Реальное кол-во уроков предмета 1: ' + CAST(@t4_real AS NVARCHAR(10));
PRINT N'Устанавливаем intLessonCount = -999 вручную...';

UPDATE dbo.tblSubject SET intLessonCount = -999 WHERE intSubjectId = 1;

DECLARE @t4_after INT = (SELECT intLessonCount FROM dbo.tblSubject WHERE intSubjectId = 1);
PRINT N'intLessonCount предмета 1 после UPDATE на -999: ' + CAST(@t4_after AS NVARCHAR(10));
PRINT CASE
    WHEN @t4_after = @t4_real
    THEN N'Тест 4 ПРОЙДЕН: триггер исправил значение на ' + CAST(@t4_real AS NVARCHAR(10))
    ELSE N'Тест 4 ПРОВАЛЕН: значение = ' + CAST(@t4_after AS NVARCHAR(10))
         + N', ожидалось '                + CAST(@t4_real  AS NVARCHAR(10))
END;


-- ── Итоговое состояние ────────────────────────────────────
PRINT N'';
PRINT N'=== Итоговое состояние (все счётчики должны совпадать с фактом) ===';
SELECT
    s.intSubjectId       AS [ID],
    s.intSubjectName     AS [Предмет],
    s.intLessonCount     AS [intLessonCount],
    COUNT(l.intLessonId) AS [Факт. уроков],
    CASE
        WHEN s.intLessonCount = COUNT(l.intLessonId) THEN N'OK'
        ELSE N'РАСХОЖДЕНИЕ!'
    END                  AS [Статус]
FROM  dbo.tblSubject AS s
LEFT  JOIN dbo.tblLesson AS l ON s.intSubjectId = l.intSubjectId
GROUP BY s.intSubjectId, s.intSubjectName, s.intLessonCount
ORDER BY s.intSubjectId;
