import pygame

import game
from bullet import Bullet

# Cowboy class: represents the player character
class Cowboy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        # Character stats and attributes
        self.max_fire_rate=game.cowboy_fire_rate
        self.fire_rate = self.max_fire_rate  # Time between shots
        self.max_health = game.cowboy_max_health
        self.damage=game.cowboy_damage
        self.max_deadeye=game.cowboy_max_deadeye
        self.max_speed = 2
        #
        self.double_pistol=game.cowboy_double_pistol
        #
        self.deadeye=0
        self.health = self.max_health
        self.alive = True
        #
        self.haunted_cooldown=200

        self.scale = scale
        self.speed = self.max_speed
        self.jump = False
        self.inAir = False
        self.shoot_cooldown = 0
        self.velocity_y = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_index = 0
        self.action = 0  # Current action (0=stand, 1=walk, 2=jump, 3=fire, 4=death)



        self.image = game.cowboy_animation_list[self.action][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.flip = False  # For left/right flipping
        self.direction = 1  # 1 = right, -1 = left
        self.pos_x = float(self.rect.x)

    def update(self):
        if not self.alive:
            game.deadeye_active=False

        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        self.update_deadeye()
        if game.haunted:
            if self.haunted_cooldown > 0:
                self.haunted_cooldown -= 1
            else:
                self.haunted_cooldown = 20
                self.speed = self.max_speed
                self.fire_rate = self.max_fire_rate
                game.haunted=False
                game.blit_BG(0)

    def shoot(self):
        # Create a bullet if cooldown is over

        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.fire_rate
            new_bullet = Bullet(
                self.rect.centerx + self.rect.size[0] * 0.31 * self.direction,
                self.rect.centery + 7,
                self.direction,
            )
            game.bullet_group.add(new_bullet)





    def update_deadeye(self):
        if game.player.deadeye <= 0:
            self.set_deadeye(0)
            game.deadeye_active=False
        if game.deadeye_active:
            if game.player.deadeye > 0:
                self.deadeye -= 1

    def check_alive(self):
        # Check if the cowboy is dead
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(4)  # Death animation

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if not self.alive:
            return

        # Horizontal movement
        if moving_left and self.rect.x>-20:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right and self.rect.x<1120:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Jumping
        if self.jump and not self.inAir:
            self.velocity_y = -11
            self.jump = False
            self.inAir = True

        # Apply gravity
        self.velocity_y += game.GRAVITY
        dy += self.velocity_y

        # Ground collision
        if self.rect.bottom + dy > 620:
            dy = 620 - self.rect.bottom
            self.inAir = False
        
        

        self.pos_x += dx
        self.rect.x = int(self.pos_x)
        self.rect.y += dy

    def update_animation(self):
        # Switch between frames in the current animation
        animation_cooldown = 100
        self.image = game.cowboy_animation_list[self.action][self.animation_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.animation_index+=1
        if self.animation_index >= len(game.cowboy_animation_list[self.action]):
            if self.action==4:
                self.animation_index=len(game.cowboy_animation_list[self.action])-1
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

    def set_deadeye(self, set):
        if set==0:
            game.BG_type=0
            self.speed=self.max_speed
            for zombie in game.zombie_group:
                zombie.speed=zombie.max_speed
        elif set==1:
            if game.player.deadeye<=0:
                self.set_deadeye(0)
                return
            game.player.deadeye-=1
            game.BG_type = 1
            self.speed=self.max_speed*0.5
            for zombie in game.zombie_group:
                zombie.speed=zombie.max_speed*0.4

