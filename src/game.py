import pygame
from itertools import cycle
from ship import ship, enemy
from math import sin, cos, degrees

clock  = pygame.time.Clock()
screen = pygame.display.set_mode((700,700))

def generate_ssvep(event_num, time):
    SSVEP = pygame.USEREVENT + event_num
    pygame.time.set_timer(SSVEP, time)
    
    ssvep_on  = pygame.Surface((50, 700))
    ssvep_off = pygame.Surface((50, 700))
    ssvep_on.fill((255,255,255))
    ssvep_off.fill((0, 0, 0))
    
    ssvep_surfaces = cycle([ssvep_on, ssvep_off])
    ssvep_surface  = next(ssvep_surfaces)
    return SSVEP, ssvep_surfaces, ssvep_surface

def render_text(msg, size):
    select_font = pygame.font.Font('../assets/ms_reg.ttf', size)
    return select_font.render(msg, True, (255,255,255))

def calibrate():
    done = False # game state

    screen = pygame.display.set_mode((700,700))
    
    SSVEP1, ssvep_surfaces1, ssvep_surface1 = generate_ssvep(0, 100)
    SSVEP2, ssvep_surfaces2, ssvep_surface2 = generate_ssvep(1, 40)
    
    look_left     = render_text("Look at the left flashing light",20)
    look_center   = render_text("Look at the center of the screen", 20)
    look_right    = render_text("Look at the right flashing light", 20)
    text_surfaces = cycle([look_left, look_center, look_right])
    text_surface  = next(text_surfaces)

    TRIAL = pygame.USEREVENT + 2
    pygame.time.set_timer(TRIAL, 5000) 
    num_trials = 1 * 3 
    i = 1
    while (not done) and (i <= num_trials):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == SSVEP1:
                ssvep_surface1 = next(ssvep_surfaces1)
            if event.type == SSVEP2:
                ssvep_surface2 = next(ssvep_surfaces2)
            if event.type == TRIAL:
                text_surface = next(text_surfaces)
                i += 1

        screen.fill((0, 0, 0))
        screen.blit(ssvep_surface1, (0, 0))
        screen.blit(ssvep_surface2, (650, 0))
        screen.blit(text_surface, (200, 200))
        pygame.display.flip()
        clock.tick(60)

    think_active  = render_text("Think about moving wildly, loud noises, etc.",20)
    think_neutral = render_text("Think normally", 20)
    think_passive = render_text("Think about nothing, clear your mind", 20)
    text_surfaces = cycle([think_active, think_neutral, think_passive])
    text_surface  = next(text_surfaces)

    TRIAL = pygame.USEREVENT + 2
    pygame.time.set_timer(TRIAL, 5000)
    num_trials = 1 * 3
    i = 1
    while not done and (i < num_trials + 1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == TRIAL:
                text_surface = next(text_surfaces)
                i += 1

        screen.fill((0, 0, 0))
        screen.blit(text_surface, (200, 200))
        pygame.display.flip()
        clock.tick(60)
            
def gameplay():
    done = False # game state

    all_sprites = pygame.sprite.Group()
    ship1       = ship()
    all_sprites.add(ship1)
    
    enemies = pygame.sprite.Group() 
    for i in range(0,2):
        e = enemy(True)
        all_sprites.add(e)
    for i in range(0,2):
        e = enemy(False)
        all_sprites.add(e)

    screen = pygame.display.set_mode((700,700))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        all_sprites.update()

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
 
        pygame.display.flip()
        clock.tick(60)

def main():
    pygame.init()
    pygame.display.set_caption('Think-Blast')
    done = False

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
        
        title = render_text("Think-Blast", 50)
        screen.blit(title, (200,50))

        option_quit = render_text("Press q to Quit", 20)
        option_play = render_text("Press p to Play", 20)
        option_cal  = render_text("Press c to Calibrate", 20)

        screen.blit(option_play, (200, 120))
        screen.blit(option_cal, (200, 140))
        screen.blit(option_quit, (200, 160))
       
        pygame.display.flip() 
        clock.tick(60)

if __name__ == '__main__':
    main()
