import pygame
import game
black=(0,0,0)
class Button:
    
    def __init__(self,x,y,image,scale,cooldown=100):
        width=image.get_width()
        height=image.get_height()
        self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False
        self.last_click_time = 0
        self.cooldown = cooldown
    #Butonu cizip fare ile uzerine gelindiginde tiklanabilir hale getirir
    def draw(self,surface):
        action=False
        position=pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                if current_time - self.last_click_time > self.cooldown:
                    self.last_click_time = current_time
                    self.clicked=True
                    action=True
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False
        surface.blit(self.image,(self.rect.x,self.rect.y))

        return action
    
class ScreenFade():
    def __init__(self,direction,colour,speed):
        self.direction=direction
        self.colour=colour
        self.speed=speed
        self.fade_counter=0
    
    #Ekrana fade efekti uygular
    def fade(self):
        fade_complete=False
        self.fade_counter += self.speed
        pygame.draw.rect(game.screen,self.colour,(0,0,game.SCREEN_WIDTH,0+self.fade_counter))
        if self.fade_counter>=game.SCREEN_WIDTH:
            fade_complete=True
        return fade_complete

class HealthBar():
    def __init__(self,x,y,width,height,hp,max_hp):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hp=hp
        self.max_hp=max_hp
    #Ekrana can bari cizer
    def draw(self,surface):
        ratio=self.hp/self.max_hp
        pygame.draw.rect(surface,"red",(self.x,self.y,self.width,self.height))
        pygame.draw.rect(surface,"green",(self.x,self.y,self.width*ratio,self.height))

class DeadeyeBar():
    def __init__(self,x,y,width,height,deadeye,max_deadeye):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.deadeye=deadeye
        self.max_deadeye=max_deadeye
    #Ekrana deadeye bari cizer
    def draw(self,surface):
        
        ratio=self.deadeye/self.max_deadeye
        pygame.draw.rect(surface,"red",(self.x,self.y,self.width,self.height))
        pygame.draw.rect(surface,"yellow",(self.x,self.y,self.width*ratio,self.height))
    
