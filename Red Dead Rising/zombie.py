

import pygame

import game
from skull import Skull




# Zombie class;
class Zombie(pygame.sprite.Sprite):
    def __init__(self, type,x, y, scale):
        super().__init__()
        # Character stats and attributes
        self.type=type
        if self.type==0:
            self.max_health = game.zombie_max_health
            self.attack_rate = game.zombie_attack_rate
            self.max_speed = game.zombie_max_speed
        else:
            self.max_health = game.tank_max_health
            self.attack_rate = game.tank_attack_rate
            self.max_speed = game.tank_max_speed
        #
        self.damage = 10
        #

        #
        self.health = self.max_health
        #
        self.alive = True
        self.scale = scale
        if game.deadeye_active:
            self.speed = self.max_speed*0.4
        else:
            self.speed=self.max_speed
        self.jump = False
        self.inAir = False
        self.attack_cooldown = 0
        self.velocity_y = 0
        self.update_time = pygame.time.get_ticks()

        self.animation_index = 0
        self.action = 0  # Current action (0=stand, 1=walk, 2=death)
        self.skull_cooldown=120


        if self.type==0:
            self.image = game.zombie_animation_list[self.action][self.animation_index]
        else:
            y-=30
            self.image = game.tank_animation_list[self.action][self.animation_index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.flip = False  # For left/right flipping
        self.direction = 1  # 1 = right, -1 = left
        self.pos_x = float(self.rect.x)
        self.not_barreled=True

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        self.update_attack()
        if game.deadeye_active:
            self.speed=self.max_speed*0.4
        else:
            self.speed=self.max_speed
        self.move()




    def check_alive(self):
        # Check if the zombie is dead
        if self.health  <= 0:
            self.health = 0
            self.speed = 0

            if self.skull_cooldown==0:
                newskull = Skull(self.rect.centerx+self.direction*50, self.rect.centery + 30)
                if self.direction==-1:
                    newskull.image = pygame.transform.flip(newskull.image, True, False)
                game.skull_group.add(newskull)
                if game.player.deadeye <= game.player.max_deadeye and not game.deadeye_active:
                    game.player.deadeye += 80
                    if game.player.deadeye > game.player.max_deadeye:
                        game.player.deadeye = game.player.max_deadeye

            self.skull_cooldown-=1
            self.alive = False
            self.update_action(2)



            if self.type and self.not_barreled:
                game.barrel_quantity+=1
                self.not_barreled=False


           # Death animation

    def update_attack(self):
        prob_distance = abs(game.player.rect.x - self.rect.x)
        nearest_barrel = None


        for barrel in game.barrel_group:
            distance = abs(barrel.rect.x - self.rect.x)
            if distance < prob_distance:
                prob_distance = distance
                nearest_barrel = barrel

        distance = prob_distance
        if distance <= 60:
            if self.attack_cooldown == 0 and self.alive:
                self.attack_cooldown = self.attack_rate
                self.update_action(3)
                if nearest_barrel is None:
                    game.player.health -= self.damage
                    return
                nearest_barrel.health -= self.damage





    def move(self):
        dx = 0

        if not self.alive:
            return


        prob_distance = abs(game.player.rect.x - self.rect.x)
        index = -1


        barrels = game.barrel_group.sprites()


        for i in range(len(barrels)):
            distance = abs(barrels[i].rect.x - self.rect.x)
            if prob_distance > distance:
                prob_distance = distance
                index = i

        if index == -1:
            if abs(game.player.rect.x - self.rect.x) <= 60:
                self.update_action(3)  # melee attack
            elif game.player.rect.x > self.rect.x:
                self.update_action(1)  # walk
                dx = self.speed
                self.flip = False
                self.direction = 1
            elif game.player.rect.x < self.rect.x:
                self.update_action(1)
                dx = -self.speed
                self.flip = True
                self.direction = -1


        else:
            if abs(barrels[index].rect.x - self.rect.x) <= 60:
                self.update_action(3)  # melee attack
            elif barrels[index].rect.x > self.rect.x:
                self.update_action(1)
                dx = self.speed
                self.flip = False
                self.direction = 1
            elif barrels[index].rect.x < self.rect.x:
                self.update_action(1)
                dx = -self.speed
                self.flip = True
                self.direction = -1


        self.pos_x += dx
        self.rect.x = int(self.pos_x)

    def update_animation(self):
        # Switch between frames in the current animation
        if self.type==0:
            animation_cooldown = 100

            self.image = game.zombie_animation_list[self.action][self.animation_index]
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.animation_index += 1
            if self.animation_index >= len(game.zombie_animation_list[self.action]):
                if self.action == 2:
                    self.animation_index = len(game.zombie_animation_list[self.action]) - 1
                else:
                    self.animation_index = 0
        else:
            animation_cooldown = 100

            self.image = game.tank_animation_list[self.action][self.animation_index]
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.animation_index += 1
            if self.animation_index >= len(game.tank_animation_list[self.action]):
                if self.action == 2:
                    self.animation_index = len(game.tank_animation_list[self.action]) - 1
                else:
                    self.animation_index = 0

    def update_action(self, new_action):
        # Set a new action and reset animation
        if self.action != new_action:
            self.action = new_action
            self.animation_index = 0
            self.update_time = pygame.time.get_ticks()

    def blit(self, surface):
        # Draw the cowboy on the screen, flipping if necessary
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
