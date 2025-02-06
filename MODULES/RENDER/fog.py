import pygame as pg

class fog_of_game(pg.sprite.Sprite):
    def __init__(self, path):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load(path)
        self.image = img
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)