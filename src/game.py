import pygame
from itertools import cycle
from ship import ship, enemy
from math import sin, cos, degrees

clock = pygame.time.Clock() # global b/c it needs to be

def calibrate():
    done = False # game state

    screen = pygame.display.set_mode((700,700))
    
    SSVEP1 = pygame.USEREVENT + 0
    pygame.time.set_timer(SSVEP1, 100) 
    ssvep1_on = pygame.Surface((50, 700))
    ssvep1_on.fill((255,255,255))
    ssvep1_off = pygame.Surface((50, 700))
    ssvep1_off.fill((0, 0, 0))
    ssvep_surfaces1 = cycle([ssvep1_on, ssvep1_off])
    ssvep_surface1 = next(ssvep_surfaces1)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == SSVEP1:
                ssvep_surface1 = next(ssvep_surfaces1)

        screen.fill((0, 0, 0))
        screen.blit(ssvep_surface1, (0,0))
        pygame.display.flip()
        clock.tick(60)

def gameplay():
    done = False # game state

    ship1 = ship(350, 350, 0)
    screen = pygame.display.set_mode((700,700))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        ship1.keyboard_movement()

        screen.fill((0, 0, 0))
        screen.blit(ship1.simage, (ship1.x, ship1.y))
 
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
