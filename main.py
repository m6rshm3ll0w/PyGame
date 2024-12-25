import pygame as pg
from MODULES.init import CONFIG
from MODULES.RENDER.main import main


if __name__ == "__main__":

    pg.init()
    size = (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"])
    screen = pg.display.set_mode(size)

    main(screen)

    pg.quit()