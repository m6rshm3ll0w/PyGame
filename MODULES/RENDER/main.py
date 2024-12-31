import pygame as pg

from MODULES.MAP.generate import MAP_GENERATION
from MODULES.RENDER.MAP2IMG import map_visualise


def main(screen):

    WLD = MAP_GENERATION()
    WLD.generate_world()
    MAP = WLD.get_map()
    map_visualise(MAP)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False



