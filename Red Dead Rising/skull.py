import pygame
import game

class Skull(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = game.skull_image
        self.rect= self.image.get_rect()
        self.rect.center=(x,y)

    def update(self):
        if pygame.sprite.collide_rect(self,game.player):
            if game.player.alive:
                game.skull_quantity+=1
                self.kill()


    def blit(self,surface):
        surface.blit(self.image,self.rect)





        
    