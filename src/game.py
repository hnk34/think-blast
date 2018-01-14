import pygame
from ship import ship
from math import sin, cos, degrees

clock = pygame.time.Clock() # global b/c it needs to be

def calibrate():
    return

def gameplay():
    done = False # game state

    ship1 = ship()
    screen = pygame.display.set_mode((700,700))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: 
            ship1.move_forward()
        if pressed[pygame.K_DOWN]:
            ship1.move_backward()
        if pressed[pygame.K_LEFT]: 
            ship1.rotate_ccw()
        if pressed[pygame.K_RIGHT]:
            ship1.rotate_cw()
    
        screen.fill((0, 0, 0))
        screen.blit(ship1.rimage,(ship1.x, ship1.y), ship1.rect)
 
        pygame.display.flip()
        clock.tick(60)

def main():
    pygame.init()
    pygame.display.set_caption('Think-Blast')
    done = False

    screen = pygame.display.set_mode((700,700))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q]:
            done = True
        if pressed[pygame.K_p]:
            gameplay()
            done = True
        if pressed[pygame.K_c]:
            calibrate()

        screen.fill((0,0,0))
        
        title_font = pygame.font.Font('../assets/ms_reg.ttf', 50)
        title = title_font.render("Think-Blast", True, (255,255,255))
        screen.blit(title, (200,50))

        option_font = pygame.font.Font('../assets/ms_reg.ttf', 22)
        option_quit = option_font.render("Press q to Quit", True, (255,255,255))
        option_play = option_font.render("Press p to Play", True, (255,255,255))
        option_cal = option_font.render("Press c to Calibrate",
                                        True, (255,255,255))
        screen.blit(option_play, (200, 120))
        screen.blit(option_cal, (200, 140))
        screen.blit(option_quit, (200, 160))
       
        pygame.display.flip() 
        clock.tick(60)

if __name__ == '__main__':
    main()
