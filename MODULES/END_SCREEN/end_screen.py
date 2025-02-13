import pygame
import sqlite3
import sys
from MODULES.init import CONFIG, logger


class EndScreen:
    def __init__(self, time):
        pygame.init()

        self.count_taps = 0
        self.is_input = False

        self.time = time
        self.size = (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"])
        self.screen = pygame.display.set_mode(
            (int(self.size[0]), int(self.size[1])))
        self.WIDTH, self.HEIGHT = self.screen.get_size()

        self.image = pygame.image.load(
            CONFIG['dirs']['pictures']['end_screen'])
        self.image = pygame.transform.scale(
            self.image, (self.WIDTH, self.HEIGHT))

        self.font = pygame.font.Font(CONFIG['dirs']['fonts']['agat8'], 30)
        self.menu = CONFIG['end_screen']['menu']
        self.save = CONFIG['end_screen']['save']
        self.menu_surface = self.font.render(self.menu, True, 'white')
        self.save_surface = self.font.render(self.save, True, 'white')
        self.menu_rect = self.menu_surface.get_rect(topleft=(485, 530))
        self.save_rect = self.save_surface.get_rect(topleft=(363, 530))
        self.menu_click_area = pygame.Rect(464, 520, 115, 45)
        self.save_click_area = pygame.Rect(340, 520, 115, 45)

        self.nickname_text = self.font.render(
            CONFIG['end_screen']['nickname'], True, 'white')
        self.time_text = self.font.render(
            CONFIG['end_screen']['time'], True, 'white')

        self.nickname = ''
        self.nickname_rect = pygame.Rect(
            400, 195, 200, 40)

        self.time_display = self.font.render(
            f'{str(self.time)} s', True, (255, 255, 255))

        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 500

    def upload_data(self):
        logger.info("writing data to bd")
        con = sqlite3.connect(CONFIG['dirs']['database'])
        cur = con.cursor()
        cur.execute('''
        INSERT INTO
            results
                (nickname, time)
        VALUES
            (?, ?)
        ''', (self.nickname, self.time))
        con.commit()
        cur.close()

    def draw_transparent_rounded_rect(self, x, y, width, height, color, alpha, border_radius=0, thickness=0):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        if thickness > 0:
            pygame.draw.rect(surface, (color[0], color[1], color[2], alpha),
                             (0, 0, width, height), border_radius=border_radius, width=thickness)
        else:
            pygame.draw.rect(surface, (color[0], color[1], color[2], alpha),
                             (0, 0, width, height), border_radius=border_radius)

        self.screen.blit(surface, (x, y))

    def run(self, audio):
        logger.info("end screen is running")
        running = True
        while running:
            current_time = pygame.time.get_ticks()

            if current_time - self.cursor_timer >= self.cursor_interval:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t and not self.is_input:
                        audio.pause_unpause_music()
                    if event.key == pygame.K_BACKSPACE:
                        self.nickname = self.nickname[:-1]
                    elif len(self.nickname) <= 10 and self.is_input:
                        self.nickname += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.menu_click_area.collidepoint(event.pos):
                            return 'menu'
                        elif self.save_click_area.collidepoint(event.pos) and self.count_taps < 1 and self.nickname != "":
                            self.upload_data()
                            self.count_taps += 1
                        if self.nickname_rect.collidepoint(event.pos):
                            self.is_input = True
                        else:
                            self.is_input = False

            self.screen.blit(self.image, (0, 0))

            self.screen.blit(self.nickname_text, (230, 200))
            self.screen.blit(self.time_text, (230, 300))

            self.screen.blit(self.time_display, (400, 300))

            self.draw_transparent_rounded_rect(
                190, 165, 500, 200, (255, 255, 255), 100, 30
            )

            self.draw_transparent_rounded_rect(*self.nickname_rect, color=(255, 255, 255), alpha=255, border_radius=10, thickness=2)
            

            nickname_input_text = self.font.render(
                self.nickname, True, 'white')
            self.screen.blit(
                nickname_input_text, (self.nickname_rect.x + 5, self.nickname_rect.y + 5))

            if self.is_input and self.cursor_visible:
                cursor_pos = self.nickname_rect.x + \
                    self.font.size(self.nickname)[0] + 5
                pygame.draw.line(self.screen, 'white',
                                 (cursor_pos, self.nickname_rect.y + 5),
                                 (cursor_pos, self.nickname_rect.y + self.nickname_rect.height - 5), 2)

            self.screen.blit(self.save_surface, self.save_rect)
            self.screen.blit(self.menu_surface, self.menu_rect)

            pygame.display.flip()

        pygame.quit()
        sys.exit()
