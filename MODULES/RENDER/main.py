import pygame as pg
from MODULES.MAP.generate import generate_world


def main(screen):

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False



