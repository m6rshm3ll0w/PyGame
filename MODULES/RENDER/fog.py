import pygame as pg

class FogOfGame(pg.sprite.Sprite):
    def __init__(self, path: str) -> None:
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load(path)
        self.image = img
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0
        
        
    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)