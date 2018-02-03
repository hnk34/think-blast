import interface, pygame, render
from itertools import cycle

def calibrate(screen):
    run_ssvep_cal(screen, "./cal_ssvep", 1, 5000)
    run_mimg_cal(screen, "./cal_mimg", 1, 5000)
    ssvep_clf = interface.train_classifier("./cal_ssvep.meta")
    return ssvep_clf

def ssvep_prompts(screen):
    screen_rect = screen.get_rect()

    text1, text_rect1 = render.text("Look at the left flashing light", 20, screen_rect.center)
    text2, text_rect2 = render.text("Look at the center of the screen", 20, screen_rect.center)
    text3, text_rect3 = render.text("Look at the right flashing light", 20, screen_rect.center)

    text_surf  = next(text_surfs)
    text_rects = cycle([text_rect1, text_rect2, text_rect3])
    text_rect  = next(text_rects)
    return text_surfs, text_surf, text_rects, text_rect

def mimg_prompts(screen):
    screen_rect = screen.get_rect()

    text1, text_rect1 = render.text("Think about moving wildly, loud noises, etc.", 20, screen_rect.center)
    text2, text_rect2 = render.text("Think normally", 20, screen_rect.center)
    text3, text_rect3 = render.text("Think about nothing, clear your mind", 20, screen_rect.center)

    text_surfs = cycle([text1, text2, text3])
    text_surf  = next(text_surfs)
    text_rects = cycle([text_rect1, text_rect2, text_rect3])
    text_rect  = next(text_rects)
    return text_surfs, text_surf, text_rects, text_rect

def run_ssvep_cal(screen, cal_file, num_trials, time_per):
    screen_rect   = screen.get_rect()

    amp1          = interface.init_mushu_amp()
    amp1.start(cal_file)

    SSVEP1, ssvep_surfs1, ssvep_surf1, _ = render.ssvep(1, 8.0)
    SSVEP2, ssvep_surfs2, ssvep_surf2, _ = render.ssvep(2, 22.0)
    TRIAL = pygame.USEREVENT + 0
    pygame.time.set_timer(TRIAL, time_per)

    i = 0
    done = False
    while (i < num_trials * 3) and not done:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == SSVEP1:
                ssvep_surf1 = next(ssvep_surfs1)
            if event.type == SSVEP2:
                ssvep_surf2 = next(ssvep_surfs2)
            if event.type == TRIAL:
                text_surf = next(text_surfs)
                text_rect = next(text_rects)

         screen.fill((0,0,0))
         screen.blit(text_surf, text_rect)
         screen.blit(ssvep_surf1, (screen_rect.centerx - 50, screen_rect.centery+100))
         screen.blit(ssvep_surf2, (screen_rect.centerx + 50, screen_rect.centery+100))

         pygame.display.flip()
         clock.tick(60)

def run_mimg_cal(screen, cal_file, num_trials, time_per):
    amp1          = interface.init_mushu_amp()
    amp1.start(cal_file)

    TRIAL         = pygame.USEREVENT + 0
    pygame.time.set_timer(TRIAL, time_per)

    i = 0
    done = False
    while (i < num_trials * 3) and not done:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == TRIAL:
                text_surf = next(text_surfs)
                text_rect = next(text_rects)

         screen.fill((0,0,0))
         screen.blit(text_surf, text_rect)

         pygame.display.flip()
         clock.tick(60)
