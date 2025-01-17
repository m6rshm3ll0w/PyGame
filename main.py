import pygame as pg
from MODULES.init import CONFIG
from MODULES.RENDER.main import main

size = (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"])

if __name__ == "__main__":
    pg.init()

    scr = pg.display.set_mode((int(size[0]), int(size[1])))

    main(scr, size)

    pg.quit()