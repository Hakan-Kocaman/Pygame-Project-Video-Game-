import random

import game


wave_number = 0
wave_cooldown = 100
spawn_cooldown = 80-wave_number*2
clear_cooldown=400
wave_isSet=False
zombies = [0,0,0]

def reset():
    global wave_number, wave_cooldown, spawn_cooldown, clear_cooldown, wave_isSet, zombies
    wave_number = 0
    wave_cooldown = 100
    spawn_cooldown = 80
    clear_cooldown = 400
    wave_isSet = False
    zombies = [0, 0, 0]
    game.zombie_max_health=20
    game.zombie_attack_rate=100
    game.zombie_max_speed=1
    
    game.tank_max_health=40
    game.tank_attack_rate=100
    game.tank_max_speed=1
    
    game.soul_max_speed=2


def update():
    global wave_number
    update_zombie()
    update_tank()
    update_soul()
    update_spawn()

    if not game.player.alive:
        game.personel_best=wave_number
        wave_number=0

def update_spawn():
    global wave_cooldown
    global wave_number
    global spawn_cooldown
    global zombies
    global wave_isSet



    if zombies[0]==0 and zombies[1]==0 and zombies[2]==0:
        wave_isSet=False

    if wave_isSet:
        random_spawn()
        return

    if len(game.zombie_group)+len(game.soul_group)==0:#no zombies
        if wave_cooldown<=0:
            wave_number += 1
            zombies[0]=( 4 + int(wave_number * 1.5))# zombie 0.
            zombies[1]=(int(wave_number//4))# tank 1.
            zombies[2]=(int(wave_number//2))# soul 2.
            random_spawn()
            wave_cooldown=100
            wave_isSet=True
        else:
            wave_cooldown-=1

    check_clear()

def random_spawn():
    global spawn_cooldown
    global zombies
    if spawn_cooldown <= 0:
        zombie_type = random.randint(0, 2)
        if zombies[zombie_type] != 0:
            zombies[zombie_type] -= 1
            game.spawn(zombie_type)
            spawn_cooldown = 80
        else:
            random_spawn()
    else:
        spawn_cooldown-=1
def check_clear():
    global clear_cooldown


    for zombie in game.zombie_group:
        if zombie.alive==True:
            return
    clear_cooldown -= 1
    if clear_cooldown<=0:
        game.zombie_group.empty()
        clear_cooldown=400


def update_zombie():
    global wave_number
    game.zombie_max_health= 10 + wave_number * 2
    if game.zombie_max_speed>1.5:
        game.zombie_max_speed=1.5
        game.zombie_attack_rate=60
        return
    game.zombie_max_speed= 1.0 + wave_number * 0.05
    game.zombie_attack_rate=100-wave_number*2

def update_tank():
    global wave_number
    game.tank_max_health = 40 + (wave_number-1) * 2.5
    if game.tank_max_speed < 1.0:
        game.tank_max_speed = 1.0
        return
    game.tank_max_speed = 0.8 + (wave_number-1) * 0.05

def update_soul():
    global wave_number
    if game.soul_max_speed < 3.0:
        game.soul_max_speed = 3.0
        return
    game.soul_max_speed = 2 + wave_number * 0.05





