from ai_plane import *

if __name__ == "__main__":
    # init the game
    pygame.init()
    delay=100
    interval=50
    pygame.key.set_repeat(delay,interval)    
    clock=pygame.time.Clock()
    # main loop
    while running:
        clock.tick(30)
        screen.fill(bg_color)
        updateBullet()
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
                    player.openFire()
        setEnemy()
        judgeSprite()
        countingSystem()
        screen.blit(player.image,player.rect) 
        pygame.display.flip()
    # quit the game
    pygame.quit()
    sys.exit()
            
    
