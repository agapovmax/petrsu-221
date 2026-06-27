-- Хранимая процедура: usp_RefreshLessonCount
-- Пересчитывает столбец intLessonCount в tblSubject на основе фактических записей tblLesson.
-- Запуск: EXEC dbo.usp_RefreshLessonCount;

CREATE OR ALTER PROCEDURE dbo.usp_RefreshLessonCount    -- процедура без параметров
AS
BEGIN
    SET NOCOUNT ON; -- отключает сообщения "N row(s) affected" после каждого DML-оператора, чтобы не засорять вывод

    -- Обновляем intLessonCount для каждого предмета.
    -- Подзапрос считает строки в tblLesson, связанные с данным предметом.
    -- Для предметов без уроков COUNT(*) вернёт 0, поэтому ISNULL не нужен.
    UPDATE s    -- обновление предметов С УРОКАМИ - ставим самые актуальные
    SET s.intLessonCount = lesson_counts.cnt
    FROM tblSubject AS s
    JOIN ( -- считаем количество уроков для каждого предмета. У нас по условию лабы их по 5 на каждый
        SELECT intSubjectId, COUNT(*) AS cnt    -- 
        FROM tblLesson
        GROUP BY intSubjectId
        -- для нашей таблицы tbl.Lesson, 
        -- intLessonID  intSubjectId
        --  1	        1	2026-04-29	Циферки
        --  2	        1	2026-04-29	Сложение
        --  3	        1	2026-04-29	Вычитание
        --  4	        1	2026-04-13	Фрактал
        --  5	        1	2026-04-14	Матрицы
        --  6	        2	2026-04-10	Буковки
        --  7	        2	2026-04-11	Знаки препинания
        -- ..
        -- Получим результат запроса
        -- 1    5
        -- 2    5
        -- 3    5
        -- ...
        -- и только этим LessonID обновим данные   
    ) AS lesson_counts ON s.intSubjectId = lesson_counts.intSubjectId;

    -- Обнуляем предметы, у которых уроков нет вовсе
    -- (они не попали в JOIN выше, значит intLessonCount может быть устаревшим).
    UPDATE tblSubject
    SET intLessonCount = 0
    WHERE intSubjectId NOT IN (
        SELECT DISTINCT intSubjectId FROM tblLesson
    );  -- Находит предметы, у которых нет ни одного урока, и устанавливает intLessonCount = 0

    -- Вывод результата для проверки
    SELECT
        s.intSubjectId                          AS [ID предмета],
        s.intSubjectName                        AS [Предмет],
        s.intLessonCount                        AS [intLessonCount (обновлён)],
        COUNT(l.intLessonId)                    AS [Реальное кол-во уроков]
    FROM tblSubject s
    LEFT JOIN tblLesson l ON s.intSubjectId = l.intSubjectId
    GROUP BY s.intSubjectId, s.intSubjectName, s.intLessonCount
    ORDER BY s.intSubjectId;

    PRINT N'usp_RefreshLessonCount: intLessonCount обновлён для всех предметов.';
END;
GO

-- ============================================================
-- Проверка процедуры
-- ============================================================

-- 1. Смотрим текущее состояние ДО вызова
SELECT
    intSubjectId,
    intSubjectName,
    intLessonCount                          AS [До вызова процедуры]
FROM tblSubject
ORDER BY intSubjectId;

-- 2а. Заполняем NULL — имитируем ситуацию когда столбец не был заполнен никогда
--     (например, после ALTER TABLE ADD COLUMN без DEFAULT)
UPDATE tblSubject SET intLessonCount = NULL;

-- 2б. Заполняем intLessonCount правильными данными без вызова процедуры.
-- LEFT JOIN нужен чтобы предметы без уроков тоже обновились (получат ISNULL -> 0).
-- COUNT(l.intLessonId) считает только непустые строки соединения, т.е. реальные уроки.
UPDATE s
SET s.intLessonCount = ISNULL(lesson_counts.cnt, 0)
FROM tblSubject AS s
LEFT JOIN (
    SELECT intSubjectId, COUNT(*) AS cnt
    FROM tblLesson
    GROUP BY intSubjectId
) AS lesson_counts ON s.intSubjectId = lesson_counts.intSubjectId;

-- 2в. Намеренно ломаем данные мусорным значением, чтобы убедиться что процедура восстановит и их
UPDATE tblSubject SET intLessonCount = -999;

-- 3. Запускаем процедуру — она вернёт таблицу сравнения внутри себя
EXEC dbo.usp_RefreshLessonCount;

-- 4. Итоговая проверка: intLessonCount должен совпадать с COUNT(tblLesson)
SELECT
    s.intSubjectId,
    s.intSubjectName                        AS [Предмет],
    s.intLessonCount                        AS [intLessonCount],
    COUNT(l.intLessonId)                    AS [Фактически уроков],
    CASE
        WHEN s.intLessonCount = COUNT(l.intLessonId) THEN N'OK'
        ELSE N'РАСХОЖДЕНИЕ!'
    END                                     AS [Статус]
FROM tblSubject s
LEFT JOIN tblLesson l ON s.intSubjectId = l.intSubjectId
GROUP BY s.intSubjectId, s.intSubjectName, s.intLessonCount
ORDER BY s.intSubjectId;
