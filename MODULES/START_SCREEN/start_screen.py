import pygame
from MODULES.init import CONFIG


def start_screen(screen: pygame.Surface, size: tuple[int,int], audio: AudioPlayer) -> str:
    audio.run()

    screen_width, screen_height = size

    image = pygame.image.load(CONFIG["dirs"]["pictures"]["main_menu"])
    image = pygame.transform.scale(image, (screen_width, screen_height))

    start_click_area = pygame.Rect(340, 520, 115, 45)
    best_results_click_area = pygame.Rect(464, 520, 115, 45)

    keleti = pygame.font.Font(CONFIG["dirs"]["fonts"]["keleti"], 90)
    fibberish = pygame.font.Font(CONFIG["dirs"]["fonts"]["fibberish"], 30)
    agat8 = pygame.font.Font(CONFIG["dirs"]["fonts"]["agat8"], 32)

    text_surface = keleti.render(CONFIG["start_screen"]["game_name"], True, 'white')
    authors_surface = fibberish.render(CONFIG["start_screen"]["authors"], True, 'white')
    start_surface = agat8.render(CONFIG["start_screen"]["start"], True, 'white')
    best_surface = agat8.render(CONFIG["start_screen"]["best"], True, 'white')

    text_rect = text_surface.get_rect(center=(screen_width // 2, 175))
    authors_rect = authors_surface.get_rect(center=(screen_width // 2, text_rect.bottom + 50))
    start_rect = start_surface.get_rect(topleft=(355, 530))
    best_rect = best_surface.get_rect(topleft=(487, 530))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                audio.pause_unpause_music()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    audio.pause_unpause_music()
                # if event.key == pygame.K_s:
                #     return 'end_screen'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_click_area.collidepoint(event.pos):
                        audio.stop_music()
                        return "game"
                    elif best_results_click_area.collidepoint(event.pos):
                        return 'best_results'

        screen.blit(image, (0, 0))

        screen.blit(text_surface, text_rect)
        screen.blit(authors_surface, authors_rect)
        screen.blit(start_surface, start_rect)
        screen.blit(best_surface, best_rect)

        pygame.display.flip()

    return "error"