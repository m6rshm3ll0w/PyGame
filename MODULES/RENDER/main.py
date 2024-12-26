import pygame as pg
from MODULES.MAP.generate import MAP_GENERATION


def main(screen):

    generator = MAP_GENERATION()
    MAP = generator.generate_world()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False



