import pygame,sys
from pygame.locals import *
from random import *

class bulletObj(pygame.sprite.Sprite):
    def __init__(self,image_file,location):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(image_file)
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=location
    def move(self):
        self.rect.top-=10
    def setPos(self):
        self.rect.left,self.rect.top=player.rect.left+45,player.rect.top-40
    def mySprite(self,enemy):
        global kill,score
        if pygame.sprite.collide_mask(self,enemy):
            kill=True
            score+=1
            laser_break=bulletObj('laserGreenShot.png',[self.rect.left,self.rect.top])
            enemy.rect.topleft=[choice(range(width-180)),-150]
            screen.blit(laser_break.image,laser_break.rect)
class planeObj(pygame.sprite.Sprite):
    def __init__(self,image_file,speed,location):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(image_file)
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=location
        self.speed=speed
    def turnleft(self):
        self.rect.left-=self.speed[0]
    def turnright(self):
        self.rect.left+=self.speed[0]
    def turnup(self):
        self.rect.top-=self.speed[0]
    def turndown(self):
        self.rect.top+=self.speed[0]
    def biu(self,laser):
        laser.move()
    def mySprite(self,enemy):
        global lives,invisible
        if invisible>0:
            invisible-=1
        else:
            if pygame.sprite.collide_mask(self,enemy):
                invisible=100
                pygame.time.delay(500)
                player.rect.left,player.rect.top=[width//2-40,height-80]
                lives=lives-1
class enemyObj(pygame.sprite.Sprite):
    def __init__(self,image_file,speed,location):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(image_file)
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=location
        self.speed=speed
    def move(self,screen): 
        if self.rect.left<0 or self.rect.right>screen.get_width():
            self.speed[0]=-self.speed[0]
        self.rect=self.rect.move(self.speed)
# init the game
pygame.init()
delay=100
interval=50
pygame.key.set_repeat(delay,interval)
# set the initial data
kill=False
done=False
running=True
death=False
screen_size=width,height=640,720
screen=pygame.display.set_mode(screen_size)
pygame.display.set_caption('plane game')
bg_color=[148,0,211]
clock=pygame.time.Clock()
plane_speed=[10,20]
enemy_speed=[5,10]
player=planeObj('player.png',plane_speed,[width//2-40,height-80])
laser_G=bulletObj('laserGreen.png',[player.rect.left+45,player.rect.top-40])
enemy_ship=enemyObj('enemyShip.png',enemy_speed,[choice(range(width-180)),0])
enemy_ufo=enemyObj('enemyUFO.png',enemy_speed,[choice(range(width-180)),-50])
enemy_B_stone=enemyObj('meteorBig.png',enemy_speed,[choice(range(width-180)),-100])
enemy_S_stone=enemyObj('meteorSmall.png',enemy_speed,[choice(range(width-80)),-150])
# set the data for counting
lives=5
score=0
invisible=0
score_font=pygame.font.Font(None,50)
score_surf=score_font.render(str(score),1,(0,0,0))
score_pos=[10,10]
player_life=planeObj('life.png',plane_speed,[width//2-40,height-80])
# set the extra game function
def setEnemy():
    enemy_ship.move(screen)
    enemy_ufo.move(screen)
    enemy_B_stone.move(screen)
    enemy_S_stone.move(screen)
    screen.blit(enemy_ship.image,enemy_ship.rect)
    screen.blit(enemy_ufo.image,enemy_ufo.rect)
    screen.blit(enemy_B_stone.image,enemy_B_stone.rect)
    screen.blit(enemy_S_stone.image,enemy_S_stone.rect)
    if enemy_ship.rect.top>=screen.get_rect().bottom+20:
        enemy_ship.rect.topleft=[choice(range(width-180)),-100]
    if enemy_ufo.rect.top>=screen.get_rect().bottom+20:
        enemy_ufo.rect.topleft=[choice(range(width-180)),0]
    if enemy_B_stone.rect.top>=screen.get_rect().bottom+20:
        enemy_B_stone.rect.topleft=[choice(range(width-180)),-150]
    if enemy_S_stone.rect.top>=screen.get_rect().bottom+20:
        enemy_S_stone.rect.topleft=[choice(range(width-180)),-50]       
def judgeSprite():
    laser_G.mySprite(enemy_B_stone)
    player.mySprite(enemy_B_stone)
    laser_G.mySprite(enemy_S_stone)
    player.mySprite(enemy_S_stone)
    laser_G.mySprite(enemy_ship)
    player.mySprite(enemy_ship)
    laser_G.mySprite(enemy_ufo)
    player.mySprite(enemy_ufo)
def countingSystem():
    global death,running
    if lives==0:
        death=True
        player.rect.left,player.rect.top=[width+1000,height+1000]
        laser_G.rect.left,laser_G.rect.top=[width+1000,height+1000]
        final_text1="Game Over"
        final_text2="Your final score is: "+str(score)
        ft1_font=pygame.font.Font(None,70)
        ft1_surf=ft1_font.render(final_text1,1,(0,0,0))
        ft2_font=pygame.font.Font(None,50)
        ft2_surf=ft2_font.render(final_text2,1,(0,0,0))
        screen.blit(ft1_surf,[screen.get_width()//2-ft1_surf.get_width()//2,100])
        screen.blit(ft2_surf,[screen.get_width()//2-ft2_surf.get_width()//2,200])
    if not death:
        score_font=pygame.font.Font(None,50)
        score_surf=score_font.render(str(score),1,(0,0,0))
        score_pos=[10,10]
        screen.blit(score_surf,score_pos)
        for i in range(lives):
            b_width=screen.get_width()
            screen.blit(player_life.image,[b_width-60*i,20])
# main loop
while running:
    clock.tick(30)
    screen.fill(bg_color)
    if done: 
        if laser_G.rect.top>=0:
            if not kill:
                 screen.blit(laser_G.image,laser_G.rect)
                 player.biu(laser_G)
            else:
                 laser_G.setPos()   
        else:
            done=False
    for event in pygame.event.get():
        if event.type==QUIT:
            running=False
        elif event.type==KEYDOWN:
            if event.key==K_UP:
                player.turnup()
            elif event.key==K_DOWN:
                player.turndown()
            elif event.key==K_LEFT:
                player.turnleft()
            elif event.key==K_RIGHT:
                player.turnright()
            elif event.key==K_SPACE:
                done=True
                kill=False
                laser_G=bulletObj('laserGreen.png',[player.rect.left+45,player.rect.top-40])   
    setEnemy()
    judgeSprite()
    countingSystem()
    screen.blit(player.image,player.rect) 
    pygame.display.flip()
# quit the game
pygame.quit()
sys.exit()
            
    
