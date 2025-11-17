import pygame

import game


class Barrel(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.health=100
        self.image=game.barrel_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if(self.health<=0):
            self.kill()

