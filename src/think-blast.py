import pygame
import render, calibrate, game

SCREEN_HEIGHT = 700
SCREEN_WIDTH  = 1024
clock  = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    pygame.init()
    pygame.display.set_caption('Think-Blast')

    title_unscale = pygame.image.load('../assets/title.png')
    title         = pygame.transform.scale(title_unscale, (500, 200))
    title_rect    = title.get_rect(center = (SCREEN_WIDTH/2, 150))

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q]:
            done = True
        if pressed[pygame.K_p]:
            game.gameplay()
            done = True
        if pressed[pygame.K_c]:
            calibrate.calibrate(screen)

        screen_rect = screen.get_rect()
        x = screen_rect.centerx
        y = screen_rect.centery
        play, play_rect = render.text("Press p to Play", 30, (x,y))
        play_rect.top += 0
        cal, cal_rect   = render.text("Press c to Calibrate", 30, (x,y))
        cal_rect.left = play_rect.left
        cal_rect.top += 40
        quit, quit_rect = render.text("Press q to Quit", 30, (x,y))
        quit_rect.left = play_rect.left
        quit_rect.top += 80

        screen.fill((0, 0, 0))
        screen.blit(title, title_rect)
        screen.blit(play, play_rect)
        screen.blit(cal, cal_rect)
        screen.blit(quit, quit_rect)
       
        pygame.display.flip() 
        clock.tick(60)

if __name__ == '__main__':
    main()
