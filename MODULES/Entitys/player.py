import pygame as pg
from MODULES.init import CONFIG

FPS = int(CONFIG["pygame"]["FPS"])


class Player:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y
        self.speed: int = 200
        self.width: int = 20

    def draw(self, surface):
        pg.draw.rect(surface, pg.Color((255, 255, 255)), (self.x-self.width//2,
                                                          self.y-self.width//2,
                                                          self.width, self.width))

    def move(self, key, center):

        if key[pg.K_w] and not (center[1] - self.y) >= 64:
            self.y -= self.speed / int(FPS)
        if key[pg.K_s] and not (self.y - center[1]) >= 64:
            self.y += self.speed / int(FPS)
        if key[pg.K_a] and not (self.x - center[0]) >= 64:
            self.x -= self.speed / int(FPS)
        if key[pg.K_d] and not (center[0] - self.x) >= 64:
            self.x += self.speed / int(FPS)

        if (self.x - center[0]) >= 64:
            self.x -= self.speed / int(FPS) - 1
        elif (center[0] - self.x) >= 64:
            self.x += self.speed / int(FPS) - 1

        if (self.y - center[1]) >= 64:
            self.y -= self.speed / int(FPS) - 1
        elif (center[1] - self.y) >= 64:
            self.y += self.speed / int(FPS) - 1
