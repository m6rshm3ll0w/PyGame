import os
import pygame
import sys
import subprocess
import json

with open('../../DATA/settings.json', "r", encoding="UTF-8") as json_data:
    CONFIG = json.load(json_data)

size = (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"])

pygame.init()

screen = pygame.display.set_mode((int(size[0]), int(size[1])))
screen_width, screen_height = screen.get_size()

image = pygame.image.load('../../DATA/reses/start_end_pictures/start.jpg')
image = pygame.transform.scale(image, (screen_width, screen_height))

click_area = pygame.Rect(270, 455, 360, 90)

font1 = pygame.font.Font(r'..\..\DATA\fonts\CeltesSP 2.otf', 90)
font2 = pygame.font.Font(r'..\..\DATA\fonts\TheBashSingingSlashy.otf', 30)
font3 = pygame.font.Font(r'..\..\DATA\fonts\Le Mano.ttf', 60)

game_name = 'The Dungeon'
authors = 'project created by: @m6rshm3ll0w, @st0rmeed'
start = 'START'

text_surface = font1.render(game_name, True, (255, 255, 255))
authors_surface = font2.render(authors, True, (255, 255, 255))
start_surface = font3.render(start, True, (255, 255, 255))

text_rect = text_surface.get_rect(center=(screen_width // 2, 175))
authors_rect = authors_surface.get_rect(center=(screen_width // 2, text_rect.bottom + 50))
start_rect = start_surface.get_rect(center=(screen_width // 2, 504))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if click_area.collidepoint(event.pos):
                    os.chdir('../../')
                    pygame.quit()
                    subprocess.run(['python', 'main.py'], check=True)
                    sys.exit()

    screen.blit(image, (0, 0))

    screen.blit(text_surface, text_rect)
    screen.blit(authors_surface, authors_rect)
    screen.blit(start_surface, start_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
