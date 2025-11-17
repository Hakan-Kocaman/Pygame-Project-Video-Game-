

import pygame
import game
import wave
import menu
from wave import wave_number


#Ekrana yazi yazdirma
def drawText(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    game.screen.blit(img,(x,y))
#Ekrana kafa sayisi yazdirma
def drawSkull():
    skull_image=pygame.transform.flip(game.skull_image,True,False)
    game.screen.blit(skull_image,(930,0))
    drawText(f"Total Head: {game.skull_quantity}",pygame.font.SysFont("comicsansms",20,bold=True),(255,255,255)
             ,1000,25)
def drawBarrel():
    barrel_image=pygame.transform.scale(game.barrel_image,
(int(game.barrel_image.get_width() * 0.5), int(game.barrel_image.get_height() * 0.5)))
    game.screen.blit(barrel_image,(945,65))
    drawText(f"Total Barrel: {game.barrel_quantity}", pygame.font.SysFont("comicsansms", 20, bold=True), (255, 255, 255)
             , 1000, 75)
    


pygame.init()
game_paused=False
game_started=False
shop_started=False
settings_started=False
howtoplay_started=False

death_fade= menu.ScreenFade(2, (150, 0, 0), 5)

#Oyunun hangi ekranda olduguna karar veren degisken
screen_state="menu"


#Gerekli buton resimlerini yukleme
img_menubutton=pygame.image.load("image/buttons/Menu_Button.png").convert_alpha()
menu_button=menu.Button(450,300,img_menubutton,0.5)

img_shopbutton=pygame.image.load("image/buttons/Shop_Button.png").convert_alpha()
shop_button=menu.Button(190,300,img_shopbutton,0.2)

img_playbutton=pygame.image.load("image/buttons/Play_Button.png").convert_alpha()
play_button=menu.Button(190,100,img_playbutton,0.5)

img_settingsbutton=pygame.image.load("image/buttons/Settings_Button.png").convert_alpha()
settings_button=menu.Button(190,200,img_settingsbutton,0.5)

img_howtoplaybutton=pygame.image.load("image/buttons/Controls_Button.png").convert_alpha()
howtoplay_button=menu.Button(190,400,img_howtoplaybutton,0.5)

img_backsquarebutton=pygame.image.load("image/buttons/BackSquare_Button.png").convert_alpha()
backsquare_button=menu.Button(50,50,img_backsquarebutton,0.5)

img_arrowbutton=pygame.image.load("image/buttons/Arrow_Button.png").convert_alpha()
arrow_button=menu.Button(450,100,img_arrowbutton,0.5)

img_retrybutton=pygame.image.load("image/buttons/Retry_Button.png").convert_alpha()
retry_button=menu.Button(495,415,img_retrybutton,0.2)


# Game loop
music_player = game.Music()
run = True
while run:

    game.clock.tick(game.FPS)


    
    #Menu ekrani
    if screen_state == "menu":
        game.blit_BG(3)
        if play_button.draw(game.screen):
            screen_state = "game"
        if shop_button.draw(game.screen):
            screen_state = "shop"
        if settings_button.draw(game.screen):
            screen_state = "settings"
        if howtoplay_button.draw(game.screen):
            screen_state = "howtoplay"
             
    #Magaza ekrani
    elif screen_state == "shop":
        game.blit_BG(3)
        upgrade=int(game.cowboy_damage*0.1)
        drawSkull()


        drawText(f"Max Health: {game.player.max_health}",pygame.font.SysFont("comicsansms",20,bold=True),(255,255,255),160,250)
        drawText(f"({upgrade})",pygame.font.SysFont("comicsansms",20,bold=True),(255,255,255),415,250)
        arrow_button=menu.Button(370,250,img_arrowbutton,0.3)
        if arrow_button.draw(game.screen):
            if game.skull_quantity>=upgrade and game.skull_quantity>0:
                game.player.max_health+=10
                game.player.health+=10
                game.skull_quantity-=upgrade
        

        drawText(f"Damage: {game.player.damage}",pygame.font.SysFont("comicsansms",20,bold=True),(255,255,255),160,300)
        drawText(f"({upgrade})",pygame.font.SysFont("comicsansms",20,bold=True),(255,255,255),415,300)
        arrow_button1=menu.Button(370,300,img_arrowbutton,0.3)
        if arrow_button1.draw(game.screen):
            if game.skull_quantity>=upgrade and game.skull_quantity>0:
                game.player.damage+=1
                game.skull_quantity-=upgrade

        updated_fire_rate =  51 - game.player.fire_rate
        drawText(f"Fire rate: {updated_fire_rate}",pygame.font.SysFont("comicsansms",20,bold=True),(255,255,255),160,350)
        drawText(f"({upgrade})",pygame.font.SysFont("comicsansms",20,bold=True),(255,255,255),415,350)
        arrow_button2=menu.Button(370,350,img_arrowbutton,0.3)
        if arrow_button2.draw(game.screen):
            if game.skull_quantity>=upgrade and game.skull_quantity>0:
                game.player.fire_rate-=1  
                game.skull_quantity-=upgrade
          
        if backsquare_button.draw(game.screen):
            screen_state = "menu"
            
        
            

    #Ayarlar ekrani
    elif screen_state == "settings":
        game.blit_BG(3)
        drawText(f"Volume",pygame.font.SysFont("comicsansms",20,bold=True),(255,255,255),415,350)
        arrow_button1=menu.Button(375,350,pygame.transform.flip(img_arrowbutton,True,False),0.3)
        drawText(f"{int(game.music.volume*10)}",pygame.font.SysFont("comicsansms",20,bold=True),(255,255,255),354,350)
        arrow_button2=menu.Button(330,350,img_arrowbutton,0.3)
        if arrow_button1.draw(game.screen):
            game.music.update_volume(0.1)
        if arrow_button2.draw(game.screen):
            game.music.update_volume(-0.1)
        if backsquare_button.draw(game.screen):
            screen_state = "menu"
    #Kontroller ekrani
    elif screen_state == "howtoplay":
        game.blit_BG(3)
        game.drawControls()
        if backsquare_button.draw(game.screen):
            screen_state = "menu"
    
    
             
             
    #Oyun ekrani
    elif screen_state=="game":
        game.blit_BG(game.BG_type)
        health_bar=menu.HealthBar(50,50,150,20,game.player.health,game.player.max_health)
        health_bar.draw(game.screen)
        deadeye_bar=menu.DeadeyeBar(300,50,150,20,game.player.deadeye,game.cowboy_max_deadeye)
        deadeye_bar.draw(game.screen)
        drawSkull()
        drawBarrel()
        drawText(f"Wave: {wave.wave_number}", pygame.font.SysFont("comicsansms", 30, bold=True),
                 (255, 255, 255)
                 , 600, 30)
        #Oyun durdurulmamis ise oyuna devam et
        if not game_paused:
            game.player.update()
            game.player.move(game.moving_left, game.moving_right)
            game.player.blit(game.screen)

            if game_paused:
                drawText("Game Paused", pygame.font.SysFont("comicsansms", 40,bold=True), (255, 255, 255), 475, 220)
                if menu_button.draw(game.screen):
                    screen_state = "menu"
                    
            

            

            game.zombie_group.update()
            for zombie in game.zombie_group:
                zombie.blit(game.screen)

            game.bullet_group.update()
            game.bullet_group.draw(game.screen)

            game.skull_group.update()
            game.skull_group.draw(game.screen)

            game.barrel_group.update()
            game.barrel_group.draw(game.screen)

            game.soul_group.update()
            for soul in game.soul_group:
                soul.blit(game.screen)

            wave.update()

            # Update animation based on state
            if game.player.alive:
                if game.shoot:
                    game.player.shoot()
                    game.player.update_action(3) #Fire
                elif game.player.inAir:
                    game.player.update_action(2)  # Jump
                elif game.moving_left or game.moving_right:
                    game.player.update_action(1)  # Walk
                else:
                        game.player.update_action(0)
                    # Idle
            else:
                #Oyuncu oldugunde olum ekranini goster
                death_fade.fade()
                drawText("You Died", pygame.font.SysFont("comicsansms", 40,bold=True), (255, 255, 255), 515, 220)
                if menu_button.draw(game.screen):
                    screen_state = "menu"
                    game_paused = False
                if retry_button.draw(game.screen):
                    print("Retry clicked")
                    
                    game.reset_game()
                    wave.reset()
                    screen_state = "game"
        else:
                #Oyun durdurulmus ise durdurma ekranini goster
                drawText("Game Paused", pygame.font.SysFont("comicsansms", 40,bold=True), (255, 255, 255), 475, 220)
                if menu_button.draw(game.screen):
                    screen_state = "menu"
                    game_paused = False
                if retry_button.draw(game.screen):
                    print("Retry clicked")
                    wave.reset()
                    game_paused = False
                    game.reset_game()
                    screen_state = "game"
            
        pygame.display.update()


    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                if not game_paused:
                    game.moving_left = True
            if event.key in (pygame.K_d, pygame.K_RIGHT):
               if not game_paused:
                    game.moving_right = True
            if event.key == pygame.K_SPACE:
                if not game_paused:
                    game.shoot = True
            if event.key in (pygame.K_w, pygame.K_UP) and game.player.alive:
               if not game_paused:
                    game.player.jump = True
            if event.key == pygame.K_r:
                if not game.deadeye_active and not game_paused:
                  game.deadeye_active=True
                  game.player.set_deadeye(1)
                elif not game_paused:
                    game.deadeye_active = False
                    game.player.set_deadeye(0)
            if event.key==pygame.K_e:
                game.build_barrel()
            if event.key == pygame.K_ESCAPE:#*************************************************************************************
                game_paused = not game_paused
                
                    
                    
                
                


        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                game.moving_left = False
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                game.moving_right = False
            if event.key == pygame.K_SPACE:
                game.shoot = False
            if event.key in (pygame.K_w, pygame.K_UP) and game.player.alive:
                game.player.jump = False
    pygame.display.update()
            




# Quit the game
pygame.quit()
