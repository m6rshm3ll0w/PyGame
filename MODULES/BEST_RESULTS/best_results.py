import pygame
import sqlite3
import sys
from MODULES.init import CONFIG, logger


class ScoreTable:
    def __init__(self):
        self.CONFIG = CONFIG

        pygame.init()
        self.size = (self.CONFIG["pygame"]["width"],
                     self.CONFIG["pygame"]["height"])
        self.screen = pygame.display.set_mode(
            (int(self.size[0]), int(self.size[1])))
        self.WIDTH, self.HEIGHT = self.screen.get_size()

        self.image = pygame.image.load(
            self.CONFIG['dirs']['pictures']['best_results'])
        self.image = pygame.transform.scale(
            self.image, (self.WIDTH, self.HEIGHT))

        self.font = pygame.font.Font(self.CONFIG['dirs']['fonts']['agat8'], 30)
        self.menu = CONFIG['best_results']['menu']
        self.menu_surface = self.font.render(self.menu, True, 'white')
        self.menu_rect = self.menu_surface.get_rect(topleft=(415, 530))
        self.menu_click_area = pygame.Rect(390, 518, 120, 50)

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

        self.positions: list[int] = [
            self.TABLE_MARGIN + 70,
            self.TABLE_MARGIN + self.COLUMN_WIDTH + 50,
            self.TABLE_MARGIN + self.COLUMN_WIDTH * 2
        ]

    def get_table_data(self):
        logger.info("get data from bd")
        con = sqlite3.connect(self.CONFIG['dirs']['database'])
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
        logger.debug("drawing table")
        for i, header in enumerate(self.headers):
            text = self.font.render(header, True, self.WHITE)
            x = 0
            if i == 0:
                x1 = self.positions[1] - 140
                text_width = text.get_width()
                x = x1 - text_width - 10
            elif i == 1:
                x1 = self.positions[1]
                x = x1 + 20
            elif i == 2:
                x2 = self.positions[2] + 100
                x = x2 + 20
            self.screen.blit(text, (x, self.HEADER_HEIGHT))

        for index, (name, time) in enumerate(self.data):
            y = self.HEADER_HEIGHT + 40 + index * self.ROW_HEIGHT

            place = str(index + 1)
            text = self.font.render(place, True, self.GRAY)
            X1 = self.positions[1] - 180
            text_width = text.get_width()
            x = X1 - text_width - 10
            self.screen.blit(text, (x, y))

            text = self.font.render(name, True, self.GRAY)
            X1_line = self.positions[1]
            x = X1_line + 20
            self.screen.blit(text, (x, y))

            text = self.font.render(str(time) + ' sec', True, self.GRAY)
            X2_line = self.positions[2] + 70
            x = X2_line + 20
            self.screen.blit(text, (x, y))

        pygame.draw.line(self.screen, self.LINE_COLOR,
                         (self.positions[1] - 70, self.HEADER_HEIGHT),
                         (self.positions[1] - 70, self.HEIGHT - 120), 2)

        pygame.draw.line(self.screen, self.LINE_COLOR,
                         (self.positions[2] + 50, self.HEADER_HEIGHT),
                         (self.positions[2] + 50, self.HEIGHT - 120), 2)

        pygame.draw.line(self.screen, self.LINE_COLOR, (self.TABLE_MARGIN, self.HEADER_HEIGHT + 30),
                         (self.WIDTH - self.TABLE_MARGIN, self.HEADER_HEIGHT + 30), 2)

        for i in range(len(self.data)):
            y = self.HEADER_HEIGHT + 30 + i * self.ROW_HEIGHT
            pygame.draw.line(self.screen, self.LINE_COLOR,
                             (self.TABLE_MARGIN, y),
                             (self.WIDTH - self.TABLE_MARGIN, y), 2)

    def run(self, audio):
        logger.info("Best result screen runned")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        audio.pause_unpause_music()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.menu_click_area.collidepoint(event.pos):
                            return 'menu'

            self.screen.blit(self.image, (0, 0))
            self.screen.blit(self.menu_surface, self.menu_rect)

            self.draw_table()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
