import pygame

import game



class Soul(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.animation_index=0
        self.action=0
        self.image=game.soul_animation_list[self.action][self.animation_index]

        self.speed=game.soul_max_speed
        if game.deadeye_active:
            self.speed = game.soul_max_speed * 0.4
        self.update_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.flip = False
        self.pos_x = float(self.rect.x)
        self.alive=True
        self.death_cooldown=100

    def update(self):


        self.update_animation()
        self.check_alive()
        self.attack()
        self.move()
        if game.deadeye_active:
            self.speed = game.soul_max_speed * 0.4
        else:
            self.speed = game.soul_max_speed
        if not self.alive:
            self.death_cooldown -= 1
            if self.death_cooldown == 0:
                self.kill()




    def check_alive(self):
        # Check if the zombie is dead
        if not self.alive:
            self.speed = 0
            self.update_action(1)
            self.alive=False # Death animation




    def attack(self):
            if pygame.sprite.collide_rect(self, game.player):
                if game.player.alive and self.alive:
                    game.player.speed=game.player.max_speed*0.4
                    game.player.fire_rate=game.player.max_fire_rate*2.5
                    game.haunted=True
                    game.blit_BG(2)
                    self.update_action(1)
                    self.alive = False  # Death animation



    def move(self):
        dx = 0
        if not self.alive:
            return

        if abs(game.player.rect.x - self.rect.x) <= 60:
            self.update_action(1) # melee attack animation expected to appear in here
        elif game.player.rect.x>self.rect.x:
            self.update_action(0)
            dx = self.speed
            self.flip = False
            self.direction = 1

        elif game.player.rect.x<self.rect.x:
            self.update_action(0)
            dx = -self.speed
            self.flip = True

            self.direction = -1
        self.pos_x += dx
        self.rect.x = int(self.pos_x)

    def update_animation(self):
        # Switch between frames in the current animation

            animation_cooldown = 100





            self.image = game.soul_animation_list[self.action][self.animation_index]
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.animation_index += 1
            if self.animation_index >= len(game.soul_animation_list[self.action]):
                if self.action == 1:

                    self.animation_index = len(game.soul_animation_list[self.action]) - 1
                else:
                    self.animation_index = 0


    def update_action(self, new_action):
        # Set a new action and reset animation
        if self.action != new_action:
            self.action = new_action
            self.animation_index = 0
            self.update_time = pygame.time.get_ticks()

    def blit(self, surface):

        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)