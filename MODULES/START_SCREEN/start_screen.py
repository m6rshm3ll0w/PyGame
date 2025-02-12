import pygame
from MODULES.init import CONFIG


class StartScreen:
    def __init__(self, screen: pygame.Surface, size: tuple[int, int], audio):
        self.screen = screen
        self.size = size
        self.audio = audio

        self.screen_width, self.screen_height = size

        self.image = pygame.image.load(CONFIG["dirs"]["pictures"]["main_menu"])
        self.image = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))

        self.start_click_area = pygame.Rect(340, 520, 115, 45)
        self.best_results_click_area = pygame.Rect(464, 520, 115, 45)

        self.keleti = pygame.font.Font(CONFIG["dirs"]["fonts"]["keleti"], 90)
        self.fibberish = pygame.font.Font(CONFIG["dirs"]["fonts"]["fibberish"], 30)
        self.agat8 = pygame.font.Font(CONFIG["dirs"]["fonts"]["agat8"], 32)

        self.text_surface = self.keleti.render(CONFIG["start_screen"]["game_name"], True, 'white')
        self.authors_surface = self.fibberish.render(CONFIG["start_screen"]["authors"], True, 'white')
        self.start_surface = self.agat8.render(CONFIG["start_screen"]["start"], True, 'white')
        self.best_surface = self.agat8.render(CONFIG["start_screen"]["best"], True, 'white')

        self.text_rect = self.text_surface.get_rect(center=(self.screen_width // 2, 175))
        self.authors_rect = self.authors_surface.get_rect(center=(self.screen_width // 2, self.text_rect.bottom + 50))
        self.start_rect = self.start_surface.get_rect(topleft=(355, 530))
        self.best_rect = self.best_surface.get_rect(topleft=(487, 530))

    def run(self) -> str:
        self.audio.run()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.audio.pause_unpause_music()
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.audio.pause_unpause_music()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.start_click_area.collidepoint(event.pos):
                            self.audio.stop_music()
                            return "main_game"
                        elif self.best_results_click_area.collidepoint(event.pos):
                            return 'best_results'

            self.screen.blit(self.image, (0, 0))
            self.screen.blit(self.text_surface, self.text_rect)
            self.screen.blit(self.authors_surface, self.authors_rect)
            self.screen.blit(self.start_surface, self.start_rect)
            self.screen.blit(self.best_surface, self.best_rect)

            pygame.display.flip()

        return "error"