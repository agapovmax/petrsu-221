# -*- coding: utf-8 -*-
import pygame
import sys
import random
import time
from pygame.locals import *

# Инициализация библиотеки Pygame
pygame.init()

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Задаем параметры блоков
BLOCK_SIZE = 40
MARGIN = 5
INFO_HEIGHT = 50

# Типы блоков
VERTICAL = 0    # Вертикальная линия
HORIZONTAL = 1  # Горизонтальная линия
CORNER = 2      # Угловой

class Block:
    def __init__(self, x, y, block_type):
        self.x = x          # Координаты блока на сетке
        self.y = y
        self.type = block_type
        self.rotation = 0  # 0, 1, 2, 3 - количество поворотов на 90 градусов
        
    def rotate(self):
        self.rotation = (self.rotation + 1) % 4     # Ограничение %4, чтобы после 0,1,2,3 снова был 0
        
    def get_connections(self):
        # Возвращаем направления, в которых есть соединения (верх, право, низ, лево)
        if self.type == VERTICAL:
            if self.rotation % 2 == 0:
                return [True, False, True, False]  # Верх и низ
            else:
                return [False, True, False, True]  # Право и лево
            
        elif self.type == HORIZONTAL:
            if self.rotation % 2 == 0:
                return [False, True, False, True]  # Право и лево
            else:
                return [True, False, True, False]  # Верх и низ
            
        elif self.type == CORNER:
            if self.rotation == 0:
                return [True, True, False, False]  # Верх и право
            elif self.rotation == 1:
                return [False, True, True, False]  # Право и низ
            elif self.rotation == 2:
                return [False, False, True, True]  # Низ и лево
            else:
                return [True, False, False, True]  # Лево и верх

class Game: # Инициализируем начальные условия игры
    def __init__(self, size=10):
        self.size = size
        self.board = [[Block(x, y, random.choice([VERTICAL, HORIZONTAL, CORNER])) 
                      for x in range(size)] for y in range(size)]   # Заполняем матрицу значениями False
        self.lighted = [[False for i in range(size)] for i in range(size)] # На старте ни один из блоков не подсвечен
        self.start_time = time.time()
        self.game_time = 120  # 2 минуты
        self.game_over = False
        self.win = False
        self.solution_shown = False
        
    def reset(self, size):
        self.__init__(size)
        
    def rotate_block(self, x, y):
        if not self.game_over:
            self.board[y][x].rotate()
            self.update_lighted()
            
    def update_lighted(self):
        # Сбрасываем все подсвеченные клетки
        self.lighted = [[False for i in range(self.size)] for i in range(self.size)]
        
        # Начинаем с левого верхнего угла
        stack = [(0, 0)]
        self.lighted[0][0] = True
        
        while stack:
            x, y = stack.pop()   # Берём последнюю добавленную клетку (верхняя левая)
            
            # Проверяем все четыре направления
            connections = self.board[y][x].get_connections() # Получаем её соединения
            for i, (dx, dy) in enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)]):
                if connections[i]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        # Проверяем, есть ли соединение с соседней клеткой
                        neighbor_conn = self.board[ny][nx].get_connections()
                        if neighbor_conn[(i + 2) % 4] and not self.lighted[ny][nx]:
                            self.lighted[ny][nx] = True
                            stack.append((nx, ny))
        
        # Проверяем, все ли клетки подсвечены
        all_lighted = all(all(row) for row in self.lighted)
        if all_lighted and not self.game_over:
            self.game_over = True
            self.win = True
            
    def get_time_left(self):
        elapsed = time.time() - self.start_time
        time_left = max(0, self.game_time - elapsed)
        return time_left
        
    def update(self):
        if not self.game_over:
            time_left = self.get_time_left()
            if time_left <= 0:
                self.game_over = True
                self.win = False

class GameUI:
    def __init__(self, size=10):
        self.game = Game(size)
        self.size = size
        self.width = self.size * (BLOCK_SIZE + MARGIN) + MARGIN
        self.height = self.size * (BLOCK_SIZE + MARGIN) + MARGIN + INFO_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Light'em up!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        
    def draw_block(self, x, y, block, lighted):
        rect_x = MARGIN + x * (BLOCK_SIZE + MARGIN)
        rect_y = MARGIN + y * (BLOCK_SIZE + MARGIN) + INFO_HEIGHT
        rect = pygame.Rect(rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE)
        
        # Рисуем фон блока
        color = YELLOW if lighted else WHITE
        if self.game.game_over and not self.game.win and self.game.solution_shown and not lighted:
            color = RED
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)
        
        # Рисуем соединения
        connections = block.get_connections()
        center_x, center_y = rect_x + BLOCK_SIZE // 2, rect_y + BLOCK_SIZE // 2
        
        if connections[0]:  # Верх
            pygame.draw.line(self.screen, BLUE, (center_x, center_y), (center_x, rect_y), 3)
        if connections[1]:  # Право
            pygame.draw.line(self.screen, BLUE, (center_x, center_y), (rect_x + BLOCK_SIZE, center_y), 3)
        if connections[2]:  # Низ
            pygame.draw.line(self.screen, BLUE, (center_x, center_y), (center_x, rect_y + BLOCK_SIZE), 3)
        if connections[3]:  # Лево
            pygame.draw.line(self.screen, BLUE, (center_x, center_y), (rect_x, center_y), 3)
        
    def draw_info(self):
        time_left = self.game.get_time_left()
        minutes = int(time_left) // 60
        seconds = int(time_left) % 60
        time_text = f"Время: {minutes:02d}:{seconds:02d}\t"

        if self.game.game_over:
            if self.game.win:
                status_text = "You Win! Нажми чтобы продолжить."
            else:
                status_text = "You died! Нажми чтобы продолжить."
        else:
            status_text = "Нажимай на блоки чтобы повернуть их"
        
        time_surface = self.font.render(time_text, True, BLACK)
        status_surface = self.font.render(status_text, True, BLACK)
        
        self.screen.blit(time_surface, (10, 10))
        self.screen.blit(status_surface, (self.width // 2 - status_surface.get_width() // 2, 10))
        
    def draw_settings(self):
        self.screen.fill(WHITE)
        title = self.font.render("Light'em up! - Настройки", True, BLACK)
        size_prompt = self.font.render("Укажите размер поля (10-100):", True, BLACK)
        
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))
        self.screen.blit(size_prompt, (self.width // 2 - size_prompt.get_width() // 2, 150))
        
        pygame.display.flip()
        
    def get_size_from_user(self):
        input_text = ""
        input_active = True
        input_rect = pygame.Rect(self.width // 2 - 100, 200, 200, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        
        while input_active:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        try:
                            size = int(input_text)
                            if 10 <= size <= 100:
                                input_active = False
                                return size
                        except ValueError:
                            pass
                        input_text = ""
                    elif event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
            
            self.screen.fill(WHITE)
            self.draw_settings()
            
            # Рисуем поле ввода
            txt_surface = self.font.render(input_text, True, BLACK)
            width = max(200, txt_surface.get_width() + 10)
            input_rect.w = width
            self.screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
            pygame.draw.rect(self.screen, color, input_rect, 2)
            
            pygame.display.flip()
            self.clock.tick(30)
        
        return 10
    
    def draw(self):
        self.screen.fill(GRAY)
        
        for y in range(self.size):
            for x in range(self.size):
                self.draw_block(x, y, self.game.board[y][x], self.game.lighted[y][x])
        
        self.draw_info()
        pygame.display.flip()
        
    def handle_click(self, pos):
        if pos[1] < INFO_HEIGHT:
            return
            
        x = (pos[0] - MARGIN) // (BLOCK_SIZE + MARGIN)
        y = (pos[1] - MARGIN - INFO_HEIGHT) // (BLOCK_SIZE + MARGIN)
        
        if 0 <= x < self.size and 0 <= y < self.size:
            if self.game.game_over:
                # Начать новую игру
                self.show_settings()
            else:
                self.game.rotate_block(x, y)
    
    def show_settings(self):
        self.draw_settings()
        size = self.get_size_from_user()
        self.__init__(size)
        
    def run(self):
        self.show_settings()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        self.handle_click(event.pos)
                elif event.type == KEYDOWN:
                    if event.key == K_r and self.game.game_over and not self.game.win:
                        # Показать решение
                        self.game.solution_shown = True
                        self.game.update_lighted()
            
            self.game.update()
            self.draw()
            self.clock.tick(30)

if __name__ == "__main__":
    ui = GameUI()
    ui.run()
