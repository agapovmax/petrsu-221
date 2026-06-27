import os
import pyodbc
from itertools import groupby
from operator import itemgetter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from func import load_config, get_connection_string


# Основной JQL-запрос
SQL = """
SELECT
-------------------------------------------------
--- H1 первый заголовок - Ученик
    pupil.intPupilId                                            AS pupil_id,
    (pupil.txtPupilSurname + N' ' + pupil.txtPupilName)         AS pupil_fio,
    pupil.datBirthday                                           AS birth_date,
    pupil.txtAddress                                            AS address,
    (SELECT AVG(markH1.intMarkValue) 
        FROM tblMark markH1 
        WHERE markH1.intPupilId = pupil.intPupilId)             AS avg_all,     -- для каждого ученика считаем среднюю оценку по всем предметам
-------------------------------------------------
--- H2 второй заголовок - Предметы
    subject.intSubjectId                                          AS subj_id,
    subject.intSubjectName                                        AS subj_name,
    teacher.intTeacherName                                        AS teacher_fio,
    (SELECT AVG(markH2.intMarkValue) 
        FROM tblMark markH2
        JOIN tblLesson l3 ON markH2.intLessonId = l3.intLessonId    -- для каждого предмета считаем среднюю оценку по всем урокам, tblLesson нужен чтобы узнатьоценки по предмету
        WHERE markH2.intPupilId = pupil.intPupilId AND l3.intSubjectId = subject.intSubjectId) AS avg_subj,    -- средняя оценка по каждому предмету
------------------------------------------------
--- H3 третий заголовок - Уроки
    lesson.intLessonId                                           AS lesson_id,
    lesson.darLessonDate                                         AS lesson_date,
    lesson.txtTheme                                              AS theme,
    m.intMarkValue                                               AS mark
FROM tblPupil pupil
CROSS JOIN tblSubject subject                                             -- надо получить учеников и их предметы. Через FROM&CROSS JOIN мы получим для каждого ученика, ВСЕ предметы. 
/*
Богоявленский-Математика, Богоявленский-Информатика, Богоявленский-Литература
Щеголева-Математика, Щеголева-Информатика, Щеголева-Литератору и тд
*/
JOIN tblTeacher teacher ON subject.intTeacherId = teacher.intTeacherId    -- только строки, у которых есть совпадение в обеих таблицах
LEFT JOIN tblLesson lesson ON subject.intSubjectId = lesson.intSubjectId
LEFT JOIN tblMark m ON lesson.intLessonId = m.intLessonId AND m.intPupilId = pupil.intPupilId
ORDER BY pupil.txtPupilSurname, pupil.txtPupilName, subject.intSubjectName, lesson.darLessonDate, lesson.intLessonId
"""
# На выходе надо получить массив словарей с данными по каждому ученику.


def get_styles():
    """
    Стили
    """
    return {
        "title": ParagraphStyle("title", fontName="Arial-Bold", fontSize=16, leading=20, alignment=1, spaceAfter=10),
        "pupil_name": ParagraphStyle("pupil_name", fontName="Arial-Bold", fontSize=12, leading=16, spaceAfter=2, spaceBefore=6),
        "pupil_info": ParagraphStyle("pupil_info", fontName="Arial", fontSize=10, leading=14, spaceAfter=2),
        "subject": ParagraphStyle("subject", fontName="Arial-Bold", fontSize=10, leading=14, leftIndent=12*mm, spaceAfter=2, spaceBefore=4),
        "subject_info": ParagraphStyle("subject_info", fontName="Arial", fontSize=10, leading=14, leftIndent=12*mm, spaceAfter=2),
    }


def fmt_avg(val):
    """
    Форматирование средней оценки
    param: val - значение оценки"""
    return f"{val:.2f}" if val is not None else "—"


def fmt_mark(val):
    """Форматирование оценки"""
    return str(int(val)) if val is not None else "—"


def fetch_data(cursor):
    """Получение данных из БД"""
    cursor.execute(SQL)
    cols = [d[0] for d in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


def create_lesson_table(lessons, styles):
    """Создание таблицы уроков"""
    data = [["Дата", "Тема урока", "Оценка"]] + [
        [r["lesson_date"] or "—", r["theme"] or "—", fmt_mark(r["mark"])]
        for r in lessons if r["lesson_id"] is not None
    ]
    
    table = Table(data, colWidths=[28*mm, 105*mm, 22*mm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.transparent),
        ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Arial"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7FB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    
    # Оборачиваем с отступом
    wrapper = Table([[table]], colWidths=[A4[0] - 40*mm])
    wrapper.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 24*mm)]))
    return wrapper


def build_report(data, pdf_title, output_path):
    """
    Функция создает PDF-файл
    :param data: результат SQL-запроса
    :param pdf_title: заголовок PDF-документа
    :param output_path: путь для сохранения выходного файла
    """

    #Настройки шрифтов и стилей для использования их в pdfmetrics
    WIN_FONTS = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts")
    pdfmetrics.registerFont(TTFont("Arial", os.path.join(WIN_FONTS, "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(WIN_FONTS, "arialbd.ttf")))
    styles = get_styles()
    
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=20*mm, rightMargin=15*mm, topMargin=20*mm, bottomMargin=20*mm, title=pdf_title)
    
    story = [Paragraph(pdf_title, styles["title"])]
    
    for i, (_, pupil_rows) in enumerate(groupby(data, key=itemgetter("pupil_id"))):
        pupil_rows = list(pupil_rows)
        first = pupil_rows[0]
        
        if i > 0:
            story.append(HRFlowable(width="100%", thickness=1, color=colors.green, spaceAfter=6, spaceBefore=8))
        
        story.extend([
            Paragraph(first["pupil_fio"], styles["pupil_name"]),
            Paragraph(f"Дата рождения: <b>{first['birth_date'] or '—'}</b>", styles["pupil_info"]),
            Paragraph(f"Адрес: <b>{first['address'] or '—'}</b>", styles["pupil_info"]),
            Paragraph(f"Средняя оценка по всем предметам: <b>{fmt_avg(first['avg_all'])}</b>", styles["pupil_info"]),
            Spacer(1, 3*mm)
        ])
        
        for _, subj_rows in groupby(pupil_rows, key=itemgetter("subj_id")):
            subj_rows = list(subj_rows)
            s = subj_rows[0]
            
            story.extend([
                Paragraph(f"Предмет: {s['subj_name']}", styles["subject"]),
                Paragraph(f"Учитель: <b>{s['teacher_fio']}</b>", styles["subject_info"]),
                Paragraph(f"Средняя оценка по предмету: <b>{fmt_avg(s['avg_subj'])}</b>", styles["subject_info"]),
                Spacer(1, 1.5*mm),
                create_lesson_table(subj_rows, styles),
                Spacer(1, 3*mm)
            ])
    
    doc.build(story)
    print(f"Отчёт сохранён: {output_path}")


def main(pdf_title, debug=False):
    """
    param: pdf_title - имя файла для сохранения отчёта (без расширения)
    """
    
    config = load_config()["connection"]
    conn_str = get_connection_string(config["server_name"], config["database_name"],
                                     config["user_login"], config["user_password"])
    
    try:
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                data = fetch_data(cursor)
                if debug:
                    print(data[0])
    except pyodbc.Error as e:
        print(f"Ошибка БД: {e}")
        return
    
    if not data:
        print("Данные не найдены.")
        return
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{pdf_title}.pdf')
    build_report(data, pdf_title, output_path)


if __name__ == "__main__":
    main("Результаты обучения", debug=True)
