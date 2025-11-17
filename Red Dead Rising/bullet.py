import pygame

import game



# Bullet class: represents a bullet fired by the cowboy
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.max_speed=10
        self.speed = self.max_speed
        # Load and scale bullet image
        self.image=game.bullet_image
        self.direction = direction
        if self.direction==1:
            self.flip=False
        else:
            self.flip=True
        self.image = pygame.transform.flip(self.image, self.flip, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
            # Move the bullet in its direction
            self.rect.centerx += self.direction * self.speed

            if self.direction==-1:
                self.flip=True
            else:
                self.flip=False
            # Remove bullet if it goes off-screen
            if game.deadeye_active:
                self.speed=self.max_speed*0.4
            else:
                self.speed=self.max_speed


            if self.rect.right < 0 or self.rect.left > game.SCREEN_WIDTH:
                self.kill()
            for zombie in game.zombie_group:
                if pygame.sprite.spritecollide(zombie, game.bullet_group, False):
                    if zombie.alive:
                        zombie.health -= game.player.damage
                        self.kill()
            for soul in game.soul_group:
                if pygame.sprite.spritecollide(soul, game.bullet_group, False):
                    if soul.alive:
                        soul.alive=False
                        self.kill()






