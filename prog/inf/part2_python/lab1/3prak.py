import sys

class TextEditor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.history = []
        self.load_file()

    def load_file(self):
        with open(self.filepath, 'r') as file:
            self.lines = file.readlines()

    def save_file(self):
        with open(self.filepath, 'w') as file:
            file.writelines(self.lines)

    def insert(self, text, num_row=None, num_col=None):
        if num_row is None:
            self.lines.append(text + '\n')
        else:
            num_row = int(num_row)
            if num_col is None:
                self.lines[num_row] = self.lines[num_row].strip() + text + '\n'
            else:
                num_col = int(num_col)
                self.lines[num_row] = self.lines[num_row][:num_col] + text + self.lines[num_row][num_col:]
        self.history.append(("insert", text, num_row, num_col))

    def delete(self):
        self.history.append(("delete", list(self.lines)))
        self.lines = []

    def delrow(self, num_row):
        num_row = int(num_row)
        self.history.append(("delrow", self.lines[num_row]))
        del self.lines[num_row]

    def delcol(self, num_col):
        num_col = int(num_col)
        self.history.append(("delcol", num_col, [line[num_col] for line in self.lines if len(line) > num_col]))
        for i in range(len(self.lines)):
            if len(self.lines[i]) > num_col:
                self.lines[i] = self.lines[i][:num_col] + self.lines[i][num_col+1:]

    def swap(self, num_row_1, num_row_2):
        num_row_1, num_row_2 = int(num_row_1), int(num_row_2)
        self.history.append(("swap", num_row_1, num_row_2))
        self.lines[num_row_1], self.lines[num_row_2] = self.lines[num_row_2], self.lines[num_row_1]

    def undo(self, num_operations=1):
        for _ in range(int(num_operations)):
            if not self.history:
                break
            operation = self.history.pop()
            if operation[0] == "insert":
                _, _, num_row, _ = operation
                if num_row is None:
                    self.lines.pop()
                else:
                    self.lines[num_row] = self.lines[num_row].replace(operation[1], '', 1)
            elif operation[0] == "delete":
                self.lines = operation[1]
            elif operation[0] == "delrow":
                self.lines.append('')
            elif operation[0] == "delcol":
                num_col, chars = operation[1], operation[2]
                for i, char in enumerate(chars):
                    self.lines[i] = self.lines[i][:num_col] + char + self.lines[i][num_col:]
            elif operation[0] == "swap":
                self.swap(operation[1], operation[2])

    def show(self):
        for line in self.lines:
            print(line, end='')

    def execute_command(self, command_line):
        command = command_line.split()
        cmd = command[0]
        args = command[1:]

        if cmd == "insert":
            self.insert(*args)
        elif cmd == "del":
            self.delete()
        elif cmd == "delrow":
            if len(args) < 1:
                print("Ошибка: укажите номер строки.")
            else:
                self.delrow(*args)
        elif cmd == "delcol":
            if len(args) < 1:
                print("Ошибка: укажите номер столбца.")
            else:
                self.delcol(*args)
        elif cmd == "swap":
            if len(args) < 2:
                print("Ошибка: укажите два номера строк.")
            else:
                self.swap(*args)
        elif cmd == "undo":
            self.undo(*args)
        elif cmd == "save":
            self.save_file()
        elif cmd == "show":
            self.show()
        elif cmd == "exit":
            sys.exit()
        else:
            print(f"Неизвестная команда: {cmd}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python3 text_editor.py <путь к файлу>")
        sys.exit(1)

    filepath = sys.argv[1]
    editor = TextEditor(filepath)

    print("Введите команды для работы с текстовым редактором:\n[insert],[del],[delraw],[delcol],[swap],[undo],[save],[show],[exit]")
    while True:
        try:
            command_line = input(">>> ")
            editor.execute_command(command_line)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
