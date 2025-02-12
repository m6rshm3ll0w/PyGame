import json

import pygame

with open('./DATA/settings.json', "r", encoding="UTF-8") as json_data:
    CONFIG = json.load(json_data)

ALL_SPRITES_LIST = pygame.sprite.Group()
BLACK = (0, 0, 0)
RED = (255, 0, 0)


