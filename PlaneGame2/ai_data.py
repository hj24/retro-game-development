import pygame,sys

# set the initial data
kill,done,running,death=False,False,True,False
MODIFY_LEFT,MODIFY_TOP,MODIFY_ENE=45,40,180
ORDER=(0,-50,-100,-150)
plane_speed=[10,20]
enemy_speed=[5,10]
# set the data of screen
screen_size=width,height=640,720
screen=pygame.display.set_mode(screen_size)
pygame.display.set_caption('plane game')
bg_color=[148,0,211]
# set the data for counting
lives=5
score=0
invisible=0


