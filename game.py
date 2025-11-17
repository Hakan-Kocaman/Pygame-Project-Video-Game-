
import pygame
import random

import wave
from barrel import Barrel
from cowboy import Cowboy
from zombie import Zombie
from soul import Soul

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = int(SCREEN_WIDTH * 9 / 16)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Red Dead Rising")

# Game setup
clock = pygame.time.Clock()
GRAVITY = 0.75
FPS = 60
BG_type = 0
spawn_cooldown=0



# Game settings
personel_best=0
skull_quantity=0
barrel_quantity=0

#
cowboy_max_health=100
cowboy_fire_rate=50
cowboy_damage=10
cowboy_max_deadeye=500
cowboy_double_pistol=False
#
zombie_max_health=20
zombie_attack_rate=100
zombie_max_speed=1
#
tank_max_health=40
tank_attack_rate=100
tank_max_speed=1
#
soul_max_speed=2


# Movement and control flags
moving_left = False
moving_right = False
shoot = False
deadeye_active=False
haunted=False



# Images/Animations
bullet_image = None
skull_image= None
deadeye_icon=None
health_icon=None
barrel_image= None
cowboy_animation_list=[]
zombie_animation_list=[]
tank_animation_list=[]
soul_animation_list=[]

# Group to hold bullets
bullet_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
skull_group= pygame.sprite.Group()
soul_group= pygame.sprite.Group()
barrel_group=pygame.sprite.Group()


bg_night=pygame.image.load("background/bg_night.png")
bg_deadeye=pygame.image.load("background/bg_deadeye.png")
bg_haunted=pygame.image.load("background/bg_night.png")
bg_mainmenu=pygame.image.load("background/bg_mainmenu.png")

#Oyuna muzik ekler
class Music:
    def __init__(self):
        self.volume = 0.3
        self.load_music()
    def load_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load("audio/music_action.mp3")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1,0.0,5000)

    def update_volume(self,change):  
        self.volume = max(0, min(1, self.volume + change))
        pygame.mixer.music.set_volume(self.volume)

# Draw background depending on type
def blit_BG(type):
    global bg_night
    global bg_deadeye
    global bg_haunted
    global bg_mainmenu
    if type == 0:
        bg_night = pygame.transform.scale(bg_night,
                                            (bg_night.get_width(), bg_night.get_height()))
        screen.blit(bg_night, (0, 0))
    elif type==1:
        bg_deadeye = pygame.transform.scale(bg_deadeye,
                                            (bg_deadeye.get_width(), bg_deadeye.get_height()))
        screen.blit(bg_deadeye, (0, 0))

    elif type==2:
        bg_haunted = pygame.transform.scale(bg_haunted,
                                            (bg_haunted.get_width(), bg_haunted.get_height()))
        screen.blit(bg_haunted, (0, 0))

    else:
        bg_mainmenu = pygame.transform.scale(bg_mainmenu,
                                            (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(bg_mainmenu, (0, 0))




def drawControls():
    image_controls=pygame.image.load("image/controls.png")
    screen.blit(pygame.transform.scale(image_controls,(400,600)),(425,50))

def spawn(type):
        location=  random.choice([-30, 1230])
        if type==2:
            newsoul=Soul(location,580)
            soul_group.add(newsoul)

        else:
            newzombie = Zombie(type, location, 570, 0.1)
            zombie_group.add(newzombie)

def build_barrel():
    global barrel_quantity
    if barrel_quantity>0:
        newbarrel = Barrel( player.rect.centerx + player.rect.size[0] * 0.31 * player.direction, 580)
        barrel_group.add(newbarrel)
        barrel_quantity-=1

#Oyunu resetler
def reset_game():
    player.health = player.max_health 
    global moving_left, moving_right, shoot, deadeye_active, haunted,barrel_quantity
    moving_left = False
    moving_right = False
    shoot = False
    deadeye_active = False
    haunted = False
    zombie_group.empty()
    bullet_group.empty()
    skull_group.empty()
    soul_group.empty()
    barrel_group.empty()
    player.alive = True
    player.health = player.max_health
    player.rect.center = (550, 580)
    player.deadeye = 0
    player.inAir = False
    player.shoot_cooldown = 0
    player.action = 0
    player.update_action(0)
    barrel_quantity = 0
    wave.reset()

def save():
    pass


def cache_all():
    cache_bullet()
    cache_skull()
    cache_cowboy()
    cache_zombie()
    cache_tank()
    cache_soul()
    cache_barrel()


def cache_barrel():
    global barrel_image
    barrel_image=pygame.image.load("image/barrel.png").convert()
    barrel_image.set_colorkey((0,0,0))
    barrel_image=pygame.transform.scale(barrel_image,
(int(barrel_image.get_width() * 2.2), int(barrel_image.get_height() * 2.2)))

def cache_bullet():
    global bullet_image
    bullet_image = (pygame.image.load("image/bullet.png").convert())
    bullet_image.set_colorkey((0, 0, 0))
    bullet_image = pygame.transform.scale(bullet_image,
  (int(bullet_image.get_width() * 0.02), int(bullet_image.get_height() * 0.01)))

def cache_skull():
    global skull_image
    skull_image = (pygame.image.load("image/skull.png")).convert()
    skull_image.set_colorkey((0, 0, 0))
    skull_image = pygame.transform.scale(skull_image,
    (int(skull_image.get_width() * 3.6), int(skull_image.get_height() * 3.6)))

    

def cache_cowboy():
    global player
    animations={"stand":5,"walk":6,"jump":1,"fire":18,"death":1}

    for key,value in animations.items():
        temp_list = []
        for i in range(value):
            img = pygame.image.load(f"image/cowboy/{key}/{i}.png").convert()
            img.set_colorkey((0, 0, 0))  # Remove white background
            img = pygame.transform.scale(img, (
                int(img.get_width() * 2.2), int(img.get_height() * 2.2)))
            temp_list.append(img)
        cowboy_animation_list.append(temp_list)

def cache_zombie():
    animations={"stand":8,"walk":8,"death":8,"attack":7}

    for key,value in animations.items():
        temp_list = []
        for i in range(value):
            img = pygame.image.load(f"image/zombie/{key}/{i}.png").convert()
            img.set_colorkey((0, 0, 0))  # Remove white background
            img = pygame.transform.scale(img, (
                int(img.get_width() * 3.2), int(img.get_height() * 3.2)))
            temp_list.append(img)
        zombie_animation_list.append(temp_list)
def cache_tank():
    animations={"stand":8,"walk":8,"death":8,"attack":7}

    for key,value in animations.items():
        temp_list = []
        for i in range(value):
            img = pygame.image.load(f"image/zombie/{key}/{i}.png").convert()
            img.set_colorkey((0,0,0))  # Remove white background
            img = pygame.transform.scale(img, (
                int(img.get_width() * 5), int(img.get_height() * 5)))
            temp_list.append(img)
        tank_animation_list.append(temp_list)

def cache_soul():

    animations={"fly":4,"collide":12}

    for key,value in animations.items():
        temp_list = []
        for i in range(value):
            img = pygame.image.load(f"image/soul/{key}/{i}.png").convert()
            img.set_colorkey((0,0,0))
        
            img = pygame.transform.scale(img, (
                int(img.get_width() * 1.5), int(img.get_height() * 1.5)))
            temp_list.append(img)
        soul_animation_list.append(temp_list)


cache_all()
# Create the player
player = Cowboy(550, 570, 0.1)

music=Music()
