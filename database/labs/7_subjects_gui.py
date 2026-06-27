import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import datetime
from func import load_config, get_connection_string


# Запросы к БД
class DB:
    def __init__(self):
        config = load_config()
        s = config['connection']
        conn_str = get_connection_string(
            s['server_name'], s['database_name'],
            s['user_login'], s['user_password']
        )
        self.conn = pyodbc.connect(conn_str)

    def close(self):
        self.conn.close()

    # Предметы
    def get_subjects(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                s.intSubjectId,
                s.intSubjectName,
                s.intSubjectVolume,
                t.intTeacherName,
                COUNT(l.intLessonId) AS lesson_count,
                AVG(CAST(m.intMarkValue AS FLOAT)) AS avg_mark
            FROM tblSubject s
            JOIN tblTeacher t ON s.intTeacherId = t.intTeacherId
            LEFT JOIN tblLesson l ON s.intSubjectId = l.intSubjectId
            LEFT JOIN tblMark m ON l.intLessonId = m.intLessonId
            GROUP BY s.intSubjectId, s.intSubjectName, s.intSubjectVolume, t.intTeacherName
            ORDER BY s.intSubjectName
        """)
        return cursor.fetchall()

    # Все данные о предметах
    def get_subject_by_id(self, subject_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT intSubjectId, intSubjectName, intSubjectVolume, intTeacherId "
            "FROM tblSubject WHERE intSubjectId = ?",
            subject_id
        )
        return cursor.fetchone()
    
    # Добавлегие предмета
    def add_subject(self, name, volume, teacher_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO tblSubject (intSubjectName, intSubjectVolume, intTeacherId, intLessonCount) "
            "VALUES (?, ?, ?, 0)",
            name, volume, teacher_id
        )
        self.conn.commit()

    # Обновление данных о предмете
    def update_subject(self, subject_id, name, volume, teacher_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE tblSubject SET intSubjectName = ?, intSubjectVolume = ?, intTeacherId = ? "
            "WHERE intSubjectId = ?",
            name, volume, teacher_id, subject_id
        )
        self.conn.commit()

    # Удаление предмета
    def delete_subject(self, subject_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM tblLesson WHERE intSubjectId = ?", subject_id
        )
        count = cursor.fetchone()[0]
        if count > 0:
            raise ValueError(f"Невозможно удалить предмет: с ним связано {count} уроков.")
        cursor.execute("DELETE FROM tblSubject WHERE intSubjectId = ?", subject_id)
        self.conn.commit()

    # Преподаватели
    def get_teachers(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT intTeacherId, intTeacherName FROM tblTeacher ORDER BY intTeacherName"
        )
        return cursor.fetchall()

    # Все уроки
    def get_lessons(self, subject_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT intLessonId, darLessonDate, txtTheme "
            "FROM tblLesson WHERE intSubjectId = ? ORDER BY darLessonDate",
            subject_id
        )
        return cursor.fetchall()

    # Вся инфа об уроках
    def get_lesson_by_id(self, lesson_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT intLessonId, darLessonDate, txtTheme, intSubjectId "
            "FROM tblLesson WHERE intLessonId = ?",
            lesson_id
        )
        return cursor.fetchone()

    # Добавление нового урока
    def add_lesson(self, subject_id, date_val, theme):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO tblLesson (intSubjectId, darLessonDate, txtTheme) VALUES (?, ?, ?)",
            subject_id, date_val, theme
        )
        cursor.execute(
            "UPDATE tblSubject SET intLessonCount = "
            "(SELECT COUNT(*) FROM tblLesson WHERE intSubjectId = ?) WHERE intSubjectId = ?",
            subject_id, subject_id
        )
        self.conn.commit()

    # Удаление урока
    def delete_lesson(self, lesson_id, subject_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM tblMark WHERE intLessonId = ?", lesson_id
        )
        count = cursor.fetchone()[0]
        if count > 0:
            raise ValueError(f"Невозможно удалить урок: у него есть {count} оценок.")
        cursor.execute("DELETE FROM tblLesson WHERE intLessonId = ?", lesson_id)
        cursor.execute(
            "UPDATE tblSubject SET intLessonCount = "
            "(SELECT COUNT(*) FROM tblLesson WHERE intSubjectId = ?) WHERE intSubjectId = ?",
            subject_id, subject_id
        )
        self.conn.commit()

    # Оценки
    def get_marks_for_lesson(self, lesson_id):
        """Returns all pupils with their mark (if any) for the given lesson."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT
                p.intPupilId,
                p.txtPupilSurname + N' ' + p.txtPupilName AS full_name,
                m.intMarkId,
                m.intMarkValue,
                m.txtMarkComment
            FROM tblPupil p
            LEFT JOIN tblMark m ON p.intPupilId = m.intPupilId AND m.intLessonId = ?
            ORDER BY p.txtPupilSurname, p.txtPupilName
            """,
            lesson_id
        )
        return cursor.fetchall()

    # Обновление оценок с проверкой наличия
    def upsert_mark(self, lesson_id, pupil_id, mark_value, comment, mark_id):
        cursor = self.conn.cursor()
        if mark_id:
            cursor.execute(
                "UPDATE tblMark SET intMarkValue = ?, txtMarkComment = ? WHERE intMarkId = ?",
                mark_value, comment or None, mark_id
            )
        else:
            cursor.execute(
                "INSERT INTO tblMark (intLessonId, intPupilId, intMarkValue, txtMarkComment) "
                "VALUES (?, ?, ?, ?)",
                lesson_id, pupil_id, mark_value, comment or None
            )
        self.conn.commit()

    # Удаление оценки
    def delete_mark(self, mark_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tblMark WHERE intMarkId = ?", mark_id)
        self.conn.commit()


# Графика
def center_window(win, width, height):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - width) // 2
    y = (sh - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")


def make_label(parent, text, row, col, sticky="e", padx=8, pady=4):
    tk.Label(parent, text=text, font=("Segoe UI", 10)).grid(
        row=row, column=col, sticky=sticky, padx=padx, pady=pady
    )


# Графика с оценками
class GradesDialog(tk.Toplevel):
    def __init__(self, parent, db: DB, lesson_id: int):
        super().__init__(parent)
        self.db = db
        self.lesson_id = lesson_id

        lesson = db.get_lesson_by_id(lesson_id)
        subject = db.get_subject_by_id(lesson[3])
        teachers = {t[0]: t[1] for t in db.get_teachers()}
        teacher_name = teachers.get(subject[3], "—")

        self.title("Оценки за урок")
        center_window(self, 640, 500)
        self.resizable(False, False)
        self.grab_set()

        # Информация
        info = tk.LabelFrame(self, text="Информация", font=("Segoe UI", 10, "bold"), padx=8, pady=6)
        info.pack(fill="x", padx=12, pady=(10, 4))

        labels = [
            ("Предмет:", subject[1]),
            ("Учитель:", teacher_name),
            ("Дата урока:", lesson[1].strftime("%d.%m.%Y") if lesson[1] else ""),
            ("Тема:", lesson[2] or ""),
        ]
        for i, (lbl, val) in enumerate(labels):
            tk.Label(info, text=lbl, font=("Segoe UI", 10, "bold"), anchor="e").grid(
                row=i // 2, column=(i % 2) * 2, sticky="e", padx=(4, 2), pady=2
            )
            tk.Label(info, text=val, font=("Segoe UI", 10), anchor="w").grid(
                row=i // 2, column=(i % 2) * 2 + 1, sticky="w", padx=(0, 12), pady=2
            )

        # Обзоор
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=12, pady=4)

        cols = ("pupil", "mark", "comment")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("pupil",   text="ФИО ученика")
        self.tree.heading("mark",    text="Оценка")
        self.tree.heading("comment", text="Комментарий")
        self.tree.column("pupil",   width=220)
        self.tree.column("mark",    width=70,  anchor="center")
        self.tree.column("comment", width=280)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Выставить / изменить оценку", width=26,
                  font=("Segoe UI", 10), command=self._edit_mark).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Убрать оценку", width=16,
                  font=("Segoe UI", 10), command=self._delete_mark).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Закрыть", width=10,
                  font=("Segoe UI", 10), command=self.destroy).pack(side="left", padx=6)

        self._refresh()

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for pupil_id, full_name, mark_id, mark_val, comment in self.db.get_marks_for_lesson(self.lesson_id):
            self.tree.insert("", "end", iid=str(pupil_id), values=(
                full_name,
                mark_val if mark_val is not None else "—",
                comment or ""
            ), tags=(str(mark_id or ""),))

    def _selected_pupil(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Выбор", "Выберите ученика.", parent=self)
            return None, None
        pupil_id = int(sel[0])
        item = self.tree.item(sel[0])
        mark_id_str = item["tags"][0] if item["tags"] else ""
        mark_id = int(mark_id_str) if mark_id_str else None
        mark_val = item["values"][1]
        comment = item["values"][2]
        return pupil_id, mark_id, (mark_val if mark_val != "—" else None), comment

    def _edit_mark(self):
        result = self._selected_pupil()
        if result[0] is None:
            return
        pupil_id, mark_id, current_mark, current_comment = result
        pupil_name = self.tree.item(str(pupil_id))["values"][0]
        MarkEditDialog(self, self.db, self.lesson_id, pupil_id, pupil_name,
                       mark_id, current_mark, current_comment,
                       on_save=self._refresh)

    def _delete_mark(self):
        result = self._selected_pupil()
        if result[0] is None:
            return
        pupil_id, mark_id, *_ = result
        if mark_id is None:
            messagebox.showinfo("Удаление", "У этого ученика нет оценки за данный урок.", parent=self)
            return
        if messagebox.askyesno("Удалить оценку", "Удалить оценку у выбранного ученика?", parent=self):
            self.db.delete_mark(mark_id)
            self._refresh()


class MarkEditDialog(tk.Toplevel):
    def __init__(self, parent, db, lesson_id, pupil_id, pupil_name,
                 mark_id, current_mark, current_comment, on_save):
        super().__init__(parent)
        self.db = db
        self.lesson_id = lesson_id
        self.pupil_id = pupil_id
        self.mark_id = mark_id
        self.on_save = on_save

        self.title("Оценка ученика")
        center_window(self, 400, 230)
        self.resizable(False, False)
        self.grab_set()

        frm = tk.Frame(self, padx=16, pady=12)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Ученик:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="e", pady=4)
        tk.Label(frm, text=pupil_name, font=("Segoe UI", 10)).grid(row=0, column=1, sticky="w", pady=4, padx=8)

        tk.Label(frm, text="Оценка (1–5):", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="e", pady=4)
        self.spin_mark = ttk.Spinbox(frm, from_=1, to=5, width=5, font=("Segoe UI", 10))
        if current_mark is not None:
            self.spin_mark.set(int(current_mark))
        else:
            self.spin_mark.set(5)
        self.spin_mark.grid(row=1, column=1, sticky="w", pady=4, padx=8)

        tk.Label(frm, text="Комментарий:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="ne", pady=4)
        self.txt_comment = tk.Text(frm, width=28, height=3, font=("Segoe UI", 10))
        if current_comment:
            self.txt_comment.insert("1.0", current_comment)
        self.txt_comment.grid(row=2, column=1, sticky="w", pady=4, padx=8)

        btn_frm = tk.Frame(frm)
        btn_frm.grid(row=3, column=0, columnspan=2, pady=8)
        tk.Button(btn_frm, text="Сохранить", width=12, font=("Segoe UI", 10),
                  command=self._save).pack(side="left", padx=6)
        tk.Button(btn_frm, text="Отменить", width=12, font=("Segoe UI", 10),
                  command=self.destroy).pack(side="left", padx=6)

    def _save(self):
        try:
            mark_val = int(self.spin_mark.get())
            if not 1 <= mark_val <= 5:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите оценку от 1 до 5.", parent=self)
            return
        comment = self.txt_comment.get("1.0", "end").strip()
        self.db.upsert_mark(self.lesson_id, self.pupil_id, mark_val, comment, self.mark_id)
        self.on_save()
        self.destroy()


# Процесс добавления урока
class AddLessonDialog(tk.Toplevel):
    def __init__(self, parent, db: DB, subject_id: int, on_save):
        super().__init__(parent)
        self.db = db
        self.subject_id = subject_id
        self.on_save = on_save

        subject = db.get_subject_by_id(subject_id)
        teachers = {t[0]: t[1] for t in db.get_teachers()}
        teacher_name = teachers.get(subject[3], "—")

        self.title("Добавить урок")
        center_window(self, 440, 300)
        self.resizable(False, False)
        self.grab_set()

        frm = tk.Frame(self, padx=16, pady=12)
        frm.pack(fill="both", expand=True)

        # Данные только для вывода
        info = tk.LabelFrame(frm, text="Предмет (информация)", font=("Segoe UI", 9), padx=8, pady=4)
        info.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        tk.Label(info, text=f"Название: {subject[1]}  |  Учитель: {teacher_name}",
                 font=("Segoe UI", 10)).pack(anchor="w")

        # Дата урока в русском формате
        tk.Label(frm, text="Дата урока (ДД.ММ.ГГГГ):", font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="e", pady=6)
        self.ent_date = ttk.Entry(frm, width=16, font=("Segoe UI", 10))
        self.ent_date.insert(0, datetime.date.today().strftime("%d.%m.%Y"))
        self.ent_date.grid(row=1, column=1, sticky="w", pady=6, padx=8)

        # Тема урока
        tk.Label(frm, text="Тема урока:", font=("Segoe UI", 10)).grid(
            row=2, column=0, sticky="e", pady=6)
        self.ent_theme = ttk.Entry(frm, width=28, font=("Segoe UI", 10))
        self.ent_theme.grid(row=2, column=1, sticky="w", pady=6, padx=8)

        btn_frm = tk.Frame(frm)
        btn_frm.grid(row=3, column=0, columnspan=2, pady=12)
        tk.Button(btn_frm, text="Сохранить", width=12, font=("Segoe UI", 10),
                  command=self._save).pack(side="left", padx=6)
        tk.Button(btn_frm, text="Отменить", width=12, font=("Segoe UI", 10),
                  command=self.destroy).pack(side="left", padx=6)

    def _save(self):
        date_str = self.ent_date.get().strip()
        theme = self.ent_theme.get().strip()
        try:
            date_val = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите дату в формате ДД.ММ.ГГГГ.", parent=self)
            return
        if not theme:
            messagebox.showerror("Ошибка", "Введите тему урока.", parent=self)
            return
        self.db.add_lesson(self.subject_id, date_val, theme)
        self.on_save()
        self.destroy()


# Добавление и редактирование предмета
class SubjectDialog(tk.Toplevel):
    """Используем оба 'Добавить предмет' (subject_id=None) и 'Изменить данные о предмете' (subject_id=<int>)."""

    def __init__(self, parent, db: DB, subject_id, on_save):
        super().__init__(parent)
        self.db = db
        self.subject_id = subject_id
        self.on_save = on_save
        self.is_edit = subject_id is not None

        title = "Изменить данные о предмете" if self.is_edit else "Добавить предмет"
        self.title(title)

        if self.is_edit:
            center_window(self, 780, 560)
        else:
            center_window(self, 560, 260)
        self.resizable(True, True)
        self.grab_set()

        self._build_subject_fields()
        if self.is_edit:
            self._build_lessons_section()
        self._build_buttons()

        if self.is_edit:
            self._load_subject()
            self._refresh_lessons()

    # Предметы (поля)
    def _build_subject_fields(self):
        fields_frame = tk.LabelFrame(self, text="Данные о предмете",
                                     font=("Segoe UI", 10, "bold"), padx=10, pady=8)
        fields_frame.pack(fill="x", padx=12, pady=(10, 4))

        tk.Label(fields_frame, text="Название предмета:", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky="e", pady=5, padx=4)
        self.ent_name = ttk.Entry(fields_frame, width=23, font=("Segoe UI", 10))
        self.ent_name.grid(row=0, column=1, sticky="w", pady=5, padx=8)

        tk.Label(fields_frame, text="Учитель:", font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="e", pady=5, padx=4)
        self.teachers = self.db.get_teachers()
        teacher_names = [t[1] for t in self.teachers]
        self.cmb_teacher = ttk.Combobox(fields_frame, values=teacher_names,
                                        state="readonly", width=20, font=("Segoe UI", 10))
        self.cmb_teacher.grid(row=1, column=1, columnspan=3, sticky="w", pady=5, padx=8)

        tk.Label(fields_frame, text="Количество часов:", font=("Segoe UI", 10)).grid(
            row=3, column=0, sticky="e", pady=5, padx=4)
        self.spin_volume = ttk.Spinbox(fields_frame, from_=1, to=42, width=8,
                                       font=("Segoe UI", 10))
        self.spin_volume.set(0)
        self.spin_volume.grid(row=3, column=1, sticky="w", pady=5, padx=8)

    def _load_subject(self):
        row = self.db.get_subject_by_id(self.subject_id)
        if row:
            self.ent_name.delete(0, "end")
            self.ent_name.insert(0, row[1])
            self.spin_volume.set(row[2] if row[2] is not None else 0)
            # select teacher
            teacher_ids = [t[0] for t in self.teachers]
            if row[3] in teacher_ids:
                self.cmb_teacher.current(teacher_ids.index(row[3]))

    # Уроки
    def _build_lessons_section(self):
        lessons_frame = tk.LabelFrame(self, text="Проведённые уроки",
                                      font=("Segoe UI", 10, "bold"), padx=10, pady=8)
        lessons_frame.pack(fill="both", expand=True, padx=12, pady=4)

        cols = ("date", "theme")
        self.lesson_tree = ttk.Treeview(lessons_frame, columns=cols,
                                        show="headings", selectmode="browse")
        self.lesson_tree.heading("date",  text="Дата")
        self.lesson_tree.heading("theme", text="Тема")
        self.lesson_tree.column("date",  width=110, anchor="center")
        self.lesson_tree.column("theme", width=450)

        vsb = ttk.Scrollbar(lessons_frame, orient="vertical", command=self.lesson_tree.yview)
        self.lesson_tree.configure(yscrollcommand=vsb.set)
        self.lesson_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Кнопки для уроков
        lesson_btns = tk.Frame(self)
        lesson_btns.pack(fill="x", padx=12, pady=2)

        tk.Button(lesson_btns, text="Добавить урок", font=("Segoe UI", 10), width=16,
                  command=self._add_lesson).pack(side="left", padx=4)
        tk.Button(lesson_btns, text="Удалить урок", font=("Segoe UI", 10), width=16,
                  command=self._delete_lesson).pack(side="left", padx=4)
        tk.Button(lesson_btns, text="Оценки за урок", font=("Segoe UI", 10), width=16,
                  command=self._open_grades).pack(side="left", padx=4)

    def _refresh_lessons(self):
        for row in self.lesson_tree.get_children():
            self.lesson_tree.delete(row)
        for lesson in self.db.get_lessons(self.subject_id):
            date_str = lesson[1].strftime("%d.%m.%Y") if lesson[1] else ""
            self.lesson_tree.insert("", "end", iid=str(lesson[0]),
                                    values=(date_str, lesson[2] or ""))

    def _add_lesson(self):
        AddLessonDialog(self, self.db, self.subject_id, on_save=self._refresh_lessons)

    def _delete_lesson(self):
        sel = self.lesson_tree.selection()
        if not sel:
            messagebox.showwarning("Выбор", "Выберите урок для удаления.", parent=self)
            return
        lesson_id = int(sel[0])
        if messagebox.askyesno("Удалить урок",
                               "Удалить выбранный урок? Это необратимо.", parent=self):
            try:
                self.db.delete_lesson(lesson_id, self.subject_id)
                self._refresh_lessons()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e), parent=self)

    def _open_grades(self):
        sel = self.lesson_tree.selection()
        if not sel:
            messagebox.showwarning("Выбор", "Выберите урок для просмотра оценок.", parent=self)
            return
        lesson_id = int(sel[0])
        GradesDialog(self, self.db, lesson_id)

    # Основные кнопки
    def _build_buttons(self):
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Сохранить", font=("Segoe UI", 10), width=12,
                  command=self._save).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Отменить", font=("Segoe UI", 10), width=12,
                  command=self.destroy).pack(side="left", padx=6)

    def _save(self):
        name = self.ent_name.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите название предмета.", parent=self)
            return
        if len(name) > 20:
            messagebox.showerror("Ошибка", "Название предмета не должно превышать 20 символов.", parent=self)
            return
        try:
            volume = int(self.spin_volume.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество часов.", parent=self)
            return
        idx = self.cmb_teacher.current()
        if idx < 0:
            messagebox.showerror("Ошибка", "Выберите учителя.", parent=self)
            return
        teacher_id = self.teachers[idx][0]

        try:
            if self.is_edit:
                self.db.update_subject(self.subject_id, name, volume, teacher_id)
            else:
                self.db.add_subject(name, volume, teacher_id)
        except Exception as e:
            messagebox.showerror("Ошибка БД", str(e), parent=self)
            return

        self.on_save()
        if not self.is_edit:
            self.destroy()
        else:
            messagebox.showinfo("Сохранено", "Данные о предмете сохранены.", parent=self)


# Главное окно с предметами
class SubjectsWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Предметы")
        self.db = DB()
        center_window(self, 980, 480)
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._refresh()

    def _build_ui(self):
        # Toolbar
        toolbar = tk.Frame(self, pady=6)
        toolbar.pack(fill="x", padx=10)

        tk.Button(toolbar, text="Добавить предмет", font=("Segoe UI", 10),
                  width=18, command=self._add_subject).pack(side="left", padx=4)
        tk.Button(toolbar, text="Удалить предмет", font=("Segoe UI", 10),
                  width=18, command=self._delete_subject).pack(side="left", padx=4)
        tk.Button(toolbar, text="Изменить данные о предмете", font=("Segoe UI", 10),
                  width=28, command=self._edit_subject).pack(side="left", padx=4)

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=10)

        # Полный вид
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=8)

        cols = ("name", "hours", "teacher", "lessons", "avg_mark")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")

        headers = {
            "name":     ("Название предмета",         200),
            "hours":    ("Количество часов",           130),
            "teacher":  ("ФИО учителя",                220),
            "lessons":  ("Количество проведённых уроков", 190),
            "avg_mark": ("Средняя оценка",             120),
        }
        for col, (heading, width) in headers.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width,
                             anchor="center" if col != "name" and col != "teacher" else "w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal",  command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Статус
        self.status_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.status_var, anchor="w",
                 font=("Segoe UI", 9), fg="gray").pack(fill="x", padx=10, pady=(0, 4))

        # Открытие по нажатию
        self.tree.bind("<Double-1>", lambda _: self._edit_subject())

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        rows = self.db.get_subjects()
        for r in rows:
            avg = f"{r[5]:.2f}" if r[5] is not None else "—"
            self.tree.insert("", "end", iid=str(r[0]),
                             values=(r[1], r[2], r[3], r[4], avg))
        self.status_var.set(f"Записей: {len(rows)}")

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Выбор", "Выберите предмет в таблице.")
            return None
        return int(sel[0])

    def _add_subject(self):
        SubjectDialog(self, self.db, subject_id=None, on_save=self._refresh)

    def _delete_subject(self):
        subject_id = self._selected_id()
        if subject_id is None:
            return
        name = self.tree.item(str(subject_id))["values"][0]
        if messagebox.askyesno("Удалить предмет",
                               f"Удалить предмет «{name}»?\nЭто действие необратимо."):
            try:
                self.db.delete_subject(subject_id)
                self._refresh()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def _edit_subject(self):
        subject_id = self._selected_id()
        if subject_id is None:
            return
        SubjectDialog(self, self.db, subject_id=subject_id, on_save=self._refresh)

    def _on_close(self):
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = SubjectsWindow()
    app.mainloop()