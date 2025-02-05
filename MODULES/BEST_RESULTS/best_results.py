import os
import subprocess
import pygame
import sqlite3
import json
import sys

def get_table_data():
    con = sqlite3.connect('./DATA/reses/results/results.sqlite')
    cur = con.cursor()
    data = list(cur.execute('''
        SELECT 
            nickname, time
        FROM
            results
        ORDER BY
            time
    '''))
    return data[:10]

def draw_table():
    # Заголовки
    for i, header in enumerate(headers):
        text = font.render(header, True, WHITE)
        if i == 0:  # PLACE
            X1 = positions[1] - 140
            text_width = text.get_width()
            x = X1 - text_width - 10
        elif i == 1:  # NICKNAME
            X1 = positions[1]
            x = X1 + 20
        elif i == 2:  # TIME
            X2 = positions[2] + 100
            x = X2 + 20
        screen.blit(text, (x, HEADER_HEIGHT))

    # Остальное
    for index, (name, time) in enumerate(data):
        y = HEADER_HEIGHT + 40 + index * ROW_HEIGHT

        # Порядковый номер
        place = str(index + 1)
        text = font.render(place, True, GRAY)
        X1 = positions[1] - 180
        text_width = text.get_width()
        x = X1 - text_width - 10
        screen.blit(text, (x, y))

        # Имя
        text = font.render(name, True, GRAY)
        X1_line = positions[1] + 40
        x = X1_line + 20
        screen.blit(text, (x, y))

        # Время
        text = font.render(str(time) + ' sec', True, GRAY)
        X2_line = positions[2] + 105
        x = X2_line + 20
        screen.blit(text, (x, y))

    # Вертикальные линии
    pygame.draw.line(screen, LINE_COLOR,
                     (positions[1] - 70, HEADER_HEIGHT),
                     (positions[1] - 70, HEIGHT - 120), 2)

    pygame.draw.line(screen, LINE_COLOR,
                     (positions[2] + 50, HEADER_HEIGHT),
                     (positions[2] + 50, HEIGHT - 120), 2)

    # Горизонтальные линии
    for i in range(len(data)):
        y = HEADER_HEIGHT + 30 + i * ROW_HEIGHT
        pygame.draw.line(screen, LINE_COLOR,
                         (TABLE_MARGIN, y),
                         (WIDTH - TABLE_MARGIN, y), 2)

with open('./DATA/settings.json', "r", encoding="UTF-8") as json_data:
    CONFIG = json.load(json_data)

pygame.init()

size = (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"])
screen = pygame.display.set_mode((int(size[0]), int(size[1])))
WIDTH, HEIGHT = screen.get_size()

image = pygame.image.load('./DATA/reses/best_result_picture/best_result.png')
image = pygame.transform.scale(image, (WIDTH, HEIGHT))

font = pygame.font.Font(CONFIG['dirs']['fonts']['LeMano'], 30)
back = 'BACK'
back_surface = font.render(back, True, 'white')
back_rect = back_surface.get_rect(topleft=(410, 530))

back_click_area = pygame.Rect(390, 518, 120, 50)

data = get_table_data()
headers = ['PLACE', 'NICKNAME', 'TIME']

# Параметры таблицы
COLUMN_WIDTH = 250
HEADER_HEIGHT = 50
ROW_HEIGHT = 40
TABLE_MARGIN = 50

# Цвета таблицы
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LINE_COLOR = (50, 50, 50)

# Позиции колонок
positions = [
    TABLE_MARGIN + 70,  # PLACE
    TABLE_MARGIN + COLUMN_WIDTH + 50,  # NICKNAME
    TABLE_MARGIN + COLUMN_WIDTH * 2  # TIME
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if back_click_area.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.run(['python', './MODULES/START_END_SCREEN/start_screen.py'], check=True)
                    sys.exit()

    screen.blit(image, (0, 0))
    screen.blit(back_surface, back_rect)

    draw_table()

    pygame.display.flip()

pygame.quit()
sys.exit()