import pygame
from MODULES.init import CONFIG



def Start_Scr(screen, size, audio):
    audio.run()

    screen_width, screen_height = size

    image = pygame.image.load(CONFIG["dirs"]["start_screen"]["path"])
    image = pygame.transform.scale(image, (screen_width, screen_height))

    click_area = pygame.Rect(270, 455, 360, 90)

    keleti = pygame.font.Font(CONFIG["dirs"]["start_screen"]["keleti"], 90)
    fibberish = pygame.font.Font(CONFIG["dirs"]["start_screen"]["fibberish"], 30)
    agat8 = pygame.font.Font(CONFIG["dirs"]["start_screen"]["agat8"], 60)

    text_surface = keleti.render(CONFIG["start_screen"]["game_name"], True, (255, 255, 255))
    authors_surface = fibberish.render(CONFIG["start_screen"]["authors"], True, (255, 255, 255))
    start_surface = agat8.render(CONFIG["start_screen"]["start"], True, (255, 255, 255))

    text_rect = text_surface.get_rect(center=(screen_width // 2, 175))
    authors_rect = authors_surface.get_rect(center=(screen_width // 2, text_rect.bottom + 50))
    start_rect = start_surface.get_rect(center=(screen_width // 2, 504))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                audio.pause_music()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if click_area.collidepoint(event.pos):
                        audio.pause_music()
                        return "main_game"

        screen.blit(image, (0, 0))

        screen.blit(text_surface, text_rect)
        screen.blit(authors_surface, authors_rect)
        screen.blit(start_surface, start_rect)

        pygame.display.flip()