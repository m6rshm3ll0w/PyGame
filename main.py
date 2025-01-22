import gc

import pygame
import pygame as pg
from MODULES.init import CONFIG
from MODULES.RENDER.main import main as main_game

size = (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"])
f_size = (CONFIG["pygame"]["f_width"], CONFIG["pygame"]["f_height"])

if __name__ == "__main__":
    pg.init()

    gc.enable()

    if CONFIG["pygame"]["fullscreen"] == "Yes":
        scr = pg.display.set_mode((int(f_size[0]), int(f_size[1])), pygame.FULLSCREEN)
        main_game(scr, f_size)
    else:
        scr = pg.display.set_mode((int(size[0]), int(size[1])))
        main_game(scr, size)

    pg.quit()