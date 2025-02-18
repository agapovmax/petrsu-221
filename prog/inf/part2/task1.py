'''
Лабораторная работа 1 https://kappa.cs.petrsu.ru/~dimitrov/info_1/23_24/lab1.html

Робот на вход принимает координаты в формате: X, Y. Верхний левый угол имеет координату (1,1). 
Робот начинает движение с верхнего левого угла. Размеры поля, по которому может перемещаться робот 100x100.
Необходимо разработать приложение преобразования высокоуровневой программы в программу понятную для робота. 
Необходимо проверять возможность перемещения робота (выход за границы поля). 
В случае если перемещение невозможно, то необходимо сообщить об этом пользователю без вывода низкоуровневой программы.
'''
program=[[1,1]]

with open('file') as file:
    for line in file:
        print("===============")
        print("Строка", line.split())
        if 'B\n' == line:
            (direction, steps) = 'B', 1
        else:
            (direction, steps) = line.split(',')
        print("Направление", direction)
        print("Количество шагов", steps)    

        ranges = ('U', 'D', 'L', 'R', 'B')
        if direction not in ranges:
            print("Ошибка ввода")
            exit()
        
        for i in range(int(steps)): # start можно не указывать

            if direction == 'U':
                prev_position = program[-1] # Последнее значение
                print("Предыдущая позиция", prev_position)
                if prev_position[1]-int(steps) < 1:
                    print("Выход за границы сверху")
                    exit()
                program.append([prev_position[0], prev_position[1]-1])
                
            if direction == 'D':
                prev_position = program[-1] # Последнее значение
                print("Предыдущая позиция", prev_position)
                if prev_position[0]+int(steps) > 99:
                    print("Выход за границы снизу")
                    exit()
                program.append([prev_position[0], prev_position[1]+1])

            if direction == 'R':
                prev_position = program[-1] # Последнее значение
                print("Предыдущая позиция", prev_position)
                if prev_position[1]+int(steps) > 99:
                    print("Выход за границы справа")
                    exit()
                program.append([prev_position[0]+1, prev_position[1]])

            if direction == 'L':
                prev_position = program[-1] # Последнее значение
                print("Предыдущая позиция", prev_position)
                if prev_position[0]-int(steps) < 1:
                    print("Выход за границы слева")
                    exit()
                program.append([prev_position[0]-1, prev_position[1]])
            
            if direction == 'B':
                print("Координаты всех выполненных шагов до B", program)
                
                if int(steps): # если указано значение параметра B
                    prev_position = program[-(int(steps)+1)] # Последнее значение
                    print("Возврат на:", int(steps), "шагов на позицию", program[-(int(steps)+1)])
                    program.append([prev_position[0], prev_position[1]])
                else: # если не указано значение параметра B
                    prev_position = program[-1] # Последнее значение
                    print("Возврат на один шаг назад")
                    program.append([prev_position[0], prev_position[1]])

                #print("Возврат на:", program[-int(steps)])
    
    for step in program:
        print("Текущий ход: ", step[0], step[1])
