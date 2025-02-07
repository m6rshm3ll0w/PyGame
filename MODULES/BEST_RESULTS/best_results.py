import subprocess
import pygame
import sqlite3
import json
import sys


class ScoreTable:
    def __init__(self):
        with open('./DATA/settings.json', "r", encoding="UTF-8") as json_data:
            self.config = json.load(json_data)

        pygame.init()
        self.size = (self.config["pygame"]["width"], self.config["pygame"]["height"])
        self.screen = pygame.display.set_mode((int(self.size[0]), int(self.size[1])))
        self.WIDTH, self.HEIGHT = self.screen.get_size()

        self.image = pygame.image.load('./DATA/reses/best_result_picture/best_result.png')
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))

        self.font1 = pygame.font.Font(self.config['dirs']['fonts']['lemano'], 30)
        self.font2 = pygame.font.Font(self.config['dirs']['fonts']['lemano'], 30)
        self.back = 'BACK'
        self.back_surface = self.font2.render(self.back, True, 'white')
        self.back_rect = self.back_surface.get_rect(topleft=(415, 530))
        self.back_click_area = pygame.Rect(390, 518, 120, 50)

        self.headers = ['PLACE', 'NICKNAME', 'TIME']
        self.data = self.get_table_data()

        self.COLUMN_WIDTH = 250
        self.HEADER_HEIGHT = 50
        self.ROW_HEIGHT = 40
        self.TABLE_MARGIN = 50

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.LINE_COLOR = (50, 50, 50)

        self.positions = [
            self.TABLE_MARGIN + 70,
            self.TABLE_MARGIN + self.COLUMN_WIDTH + 50,
            self.TABLE_MARGIN + self.COLUMN_WIDTH * 2
        ]

    def get_table_data(self):
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
        con.close()
        return data[:10]

    def draw_table(self):
        for i, header in enumerate(self.headers):
            text = self.font1.render(header, True, self.WHITE)
            if i == 0:
                X1 = self.positions[1] - 140
                text_width = text.get_width()
                x = X1 - text_width - 10
            elif i == 1:
                X1 = self.positions[1]
                x = X1 + 20
            elif i == 2:
                X2 = self.positions[2] + 100
                x = X2 + 20
            self.screen.blit(text, (x, self.HEADER_HEIGHT))

        for index, (name, time) in enumerate(self.data):
            y = self.HEADER_HEIGHT + 40 + index * self.ROW_HEIGHT

            place = str(index + 1)
            text = self.font2.render(place, True, self.GRAY)
            X1 = self.positions[1] - 180
            text_width = text.get_width()
            x = X1 - text_width - 10
            self.screen.blit(text, (x, y))

            text = self.font2.render(name, True, self.GRAY)
            X1_line = self.positions[1] + 40
            x = X1_line + 20
            self.screen.blit(text, (x, y))

            text = self.font2.render(str(time) + ' sec', True, self.GRAY)
            X2_line = self.positions[2] + 105
            x = X2_line + 20
            self.screen.blit(text, (x, y))

        pygame.draw.line(self.screen, self.LINE_COLOR,
                         (self.positions[1] - 70, self.HEADER_HEIGHT),
                         (self.positions[1] - 70, self.HEIGHT - 120), 2)

        pygame.draw.line(self.screen, self.LINE_COLOR,
                         (self.positions[2] + 50, self.HEADER_HEIGHT),
                         (self.positions[2] + 50, self.HEIGHT - 120), 2)

        for i in range(len(self.data)):
            y = self.HEADER_HEIGHT + 30 + i * self.ROW_HEIGHT
            pygame.draw.line(self.screen, self.LINE_COLOR,
                             (self.TABLE_MARGIN, y),
                             (self.WIDTH - self.TABLE_MARGIN, y), 2)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.back_click_area.collidepoint(event.pos):
                            return 'main_menu'

            self.screen.blit(self.image, (0, 0))
            self.screen.blit(self.back_surface, self.back_rect)

            self.draw_table()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


