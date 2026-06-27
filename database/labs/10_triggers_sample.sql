-- Триггеры для поддержания целостности intLessonCount в tblSubject.
-- У нас всегда автоматом пересчитается КОЛИЧЕСТВОА уроков в tblSubject после добавления\удаления УРОКА в tblLesson.
-- Логика: после любого изменения tblLesson триггер заново считает
-- COUNT(*) уроков для затронутых предметов и записывает результат.
-- Это проще и надёжнее, чем ±1, потому что со счётчиками возиться сложнее. 

-- Зачем вообще нужно: поддержание актуальности счетчика — после вставки новых уроков автоматически обновляется intLessonCount в таблице предметов tblSubject
-- После добавления уроков пересчитываем счётчик у затронутых предметов.
-- для проверки возможны три сценария:
-- * добавление урока по предмету (провели пару, добавили в журнал)
-- * удаление уровка по предмету (интересно конечно, кто добавляет урок заранее, но все же)
-- * обновление урока по предмету (провели урок по ДРУГОМУ предмету! Жиза)


CREATE OR ALTER TRIGGER dbo.trg_tblLesson_Insert -- создаем новый триггер
ON dbo.tblLesson    -- привязываем триггер к таблице rbl.Lesson
AFTER INSERT        -- это ВАЖНО! сработает после того как данные будут добавлены
AS
BEGIN
    SET NOCOUNT ON; -- отключает сообщение "количество строк, затронутых операцией" в консоль

    UPDATE dbo.tblSubject   -- обновляем таблицу предметов
    SET    intLessonCount = (   -- для каждого предмета считаем количество уроков (COUNT(*)), где WHERE intSubjectId совпадает
               SELECT COUNT(*)
               FROM   dbo.tblLesson
               WHERE  intSubjectId = dbo.tblSubject.intSubjectId
           )    -- в итоге запишем в intLessonCount актуальное значение количества уроков
    WHERE  intSubjectId IN (SELECT DISTINCT intSubjectId FROM inserted);    -- inserted — виртуальная таблица, содержащая только что добавленные строки
        -- SELECT DISTINCT intSubjectId FROM inserted — только уникальные ИД предметов, для которых были добавлены уроки
        -- вообщем обновляем только те предметы, у которых изменилось количество уроков
END;
GO

-- После удаления уроков пересчитываем счётчик у затронутых предметов.
CREATE OR ALTER TRIGGER dbo.trg_tblLesson_Delete
ON dbo.tblLesson
AFTER DELETE    -- ВАЖНО! Дергаем ручку только после удаления строки!
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE dbo.tblSubject
    SET    intLessonCount = (
               SELECT COUNT(*)
               FROM   dbo.tblLesson
               WHERE  intSubjectId = dbo.tblSubject.intSubjectId
           )
    WHERE  intSubjectId IN (SELECT DISTINCT intSubjectId FROM deleted); -- в этот раз берем уникальные значения из виртуальной таблицы 
END;
GO
-- а вообще виртуальные таблицы интересные. Они создаются автоматически для каждого триггера INSERT, UPDATE, DELETE и существуют только в контексте выполнения триггера

-- После изменения урока пересчитываем счётчики у старого и нового предметов.
-- (объединяем intSubjectId из deleted и inserted, чтобы покрыть оба случая)
CREATE OR ALTER TRIGGER dbo.trg_tblLesson_Update
ON dbo.tblLesson
AFTER UPDATE -- после обновления!!!
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE dbo.tblSubject
    SET    intLessonCount = (
               SELECT COUNT(*)
               FROM   dbo.tblLesson
               WHERE  intSubjectId = dbo.tblSubject.intSubjectId
           )
    WHERE  intSubjectId IN (
               SELECT intSubjectId FROM deleted
               UNION
               SELECT intSubjectId FROM inserted
           ); -- тут надо обхединить уникальные значения сразу из двух виртуальных таблиц
END;
GO


-- ============================================================
-- ЧАСТЬ 2. ПРОВЕРКА ТРИГГЕРОВ
-- ============================================================

-- Если нужно посмотреть структуру tblLesson перед тестом INSERT:
-- EXEC sp_help 'dbo.tblLesson';
-- ЭТО ИМБА!!! Прям как man по команде, только по таблице! ЗАПОМНИТЬ!


-- ── 0. Исходное состояние ─────────────────────────────────
PRINT N'Что в начале до теста';
SELECT
    s.intSubjectId       AS [ID],
    s.intSubjectName     AS [Предмет],
    s.intLessonCount     AS [intLessonCount],
    COUNT(l.intLessonId) AS [Уроки по факту]
FROM  dbo.tblSubject AS s
LEFT  JOIN dbo.tblLesson AS l ON s.intSubjectId = l.intSubjectId
GROUP BY s.intSubjectId, s.intSubjectName, s.intLessonCount
ORDER BY s.intSubjectId;


-- Тесты

-- Рассчитываем, что intLessonCount предмета 9 (информатика) вырастет на 1.
PRINT N'';
PRINT N'Тестируем добавление урока: INSERT';

DECLARE @SubjectId INT = 9; -- чтобы не вводить каждый раз заново для другого предмета
--  пусть это будет 9 прдмет (Информатика, у него как раз 4 урока почему-то, видимо забыл создать в самом начале все пять)

INSERT INTO dbo.tblLesson (intSubjectId, darLessonDate, txtTheme)
VALUES (@SubjectId,'2026-05-18',N'Тест триггера'); --

SELECT  intSubjectId    AS [ID], 
        intSubjectName  AS [Предмет], 
        intLessonCount  AS [intLessonCount после INSERT]
FROM   dbo.tblSubject WHERE intSubjectId = @SubjectId;


-- Ожидаем, что intLessonCount предмета 9 уменьшится на 1.
PRINT N'';
PRINT N'Тестируем УДАЛЕНИЕ урока: DELETE';

DELETE FROM dbo.tblLesson
WHERE  intLessonId = (SELECT MAX(intLessonId) FROM dbo.tblLesson WHERE intSubjectId = @SubjectId);

SELECT intSubjectId AS [ID], intSubjectName AS [Предмет], intLessonCount AS [intLessonCount после DELETE]
FROM   dbo.tblSubject WHERE intSubjectId = @SubjectId;

-- Переносим последний урок предмета 9 → предмет 2.
-- Ожидание: счётчик предмета 9 −1, предмета 2 +1.
PRINT N'';
PRINT N'Тестируем обновление урока UPDATE (перенос урока из предмета 9 в предмет 2)';

DECLARE @MovedId INT = (SELECT MAX(intLessonId) FROM dbo.tblLesson WHERE intSubjectId = @SubjectId);
UPDATE dbo.tblLesson SET intSubjectId = 2 WHERE intLessonId = @MovedId;

SELECT intSubjectId AS [ID], intSubjectName AS [Предмет], intLessonCount AS [intLessonCount после UPDATE]
FROM   dbo.tblSubject WHERE intSubjectId IN (@SubjectId, 2)
ORDER BY intSubjectId;

-- Возвращаем урок обратно
UPDATE dbo.tblLesson SET intSubjectId = @SubjectId WHERE intLessonId = @MovedId;
PRINT N'Урок возвращаем обратно в предмет:' + CAST(@SubjectId AS VARCHAR);;


PRINT N'';
PRINT N'ИТОГ';
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
