import pygame
from itertools import cycle
from game_object import ship, enemy, bullet
from math import sin, cos, degrees
from interface import init_lsl, read_lsl, classify_buf

SCREEN_HEIGHT = 700
SCREEN_WIDTH  = 1024
SSVEP_WIDTH   = 50
clock  = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def write_cal_trial(cal_file, time, num_trial, mode):
    """
    write_cal_trial() - Write epoching data to the calibration file
    @cal_file:  The file variable for the calibration file.
    @num_trial: The trial number, which is 0, 1, or 2 for 3-class trials.
    @mode:      SSVEP or motor imagery.

    Returns: None
    """
    if mode == 0 and num_trial == 0:
        cal_file.write(str(time) + ", SSVEP LEFT\n")
    elif mode == 0 and num_trial == 1:
        cal_file.write(str(time) + ", SSVEP BASE\n")
    elif mode == 0 and num_trial == 2:
        cal_file.write(str(time) + ", SSVEP RIGHT\n")
    
    if mode == 1 and num_trial == 0:
        cal_file.write(str(time) + ", MIMG ALL\n")
    if mode == 1 and num_trial == 1:
        cal_file.write(str(time) + ", MIMG BASE\n")
    if mode == 1 and num_trial == 2:
        cal_file.write(str(time) + ", MIMG NONE\n")

def generate_ssvep(event_num, freq):
    """
    generate_ssvep() - creates SSVEP surfaces and timers
    event_num: The event number for the timer - must be unique.
    freq: The frequency of the SSVEP flashes.

    Helper function for rendering SSVEP flashes. SSVEP is rendered by switching
    between two surfaces when a certain timer event occurs.

    Return: The timer event, ssvep surfaces, and current surface.
    """
    SSVEP = pygame.USEREVENT + event_num
    time  = int(round((1.0 / freq) * 1000.0))
    pygame.time.set_timer(SSVEP, time)

    ssvep_on  = pygame.Surface((SSVEP_WIDTH, SCREEN_HEIGHT))
    ssvep_off = pygame.Surface((SSVEP_WIDTH, SCREEN_HEIGHT))
    ssvep_on.fill((255,255,255))
    ssvep_off.fill((0, 0, 0))

    ssvep_surfaces = cycle([ssvep_on, ssvep_off])
    ssvep_surface  = next(ssvep_surfaces)
    return SSVEP, ssvep_surfaces, ssvep_surface

def render_text(msg, size):
    """
    render_text() - Render text in the default font.
    @msg:  The text to display.
    @size: The font size

    Helper function for rendering text.

    Return: The text object, and the centered text rect
    """
    select_font = pygame.font.Font("../assets/prstartk.ttf", size)
    text_surf   = select_font.render(msg, True, (255,255,255))
    text_rect   = text_surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    return text_surf, text_rect

def run_calibration_set(cal_file, cal_file2, mode, num_trials, time_per):
    """
    run_calibration_set() - do a set of trials to generate a calibration dataset
    @cal_file:   The file variable for the calibration file 
    @mode:       The type of calibration to do- send 0 for SSVEP, send 1 for motor imagery
    @num_trials: The number of trials to run
    @time_per:   How long the trial prompt remains on the screen

    Generates, renders, and runs a set of calibration trials.

    Return: None
    """
    if mode == 0:
        text1, text_rect1 = render_text("Look at the left flashing light",20)
        text2, text_rect2 = render_text("Look at the center of the screen", 20)
        text3, text_rect3 = render_text("Look at the right flashing light", 20)
        SSVEP1, ssvep_surfs1, ssvep_surf1 = generate_ssvep(1, 8.0)
        SSVEP2, ssvep_surfs2, ssvep_surf2 = generate_ssvep(2, 22.0)
    elif mode == 1: # Motor imagery
        text1, text_rect1 = render_text("Think about moving wildly, loud noises, etc.",20)
        text2, text_rect2 = render_text("Think normally", 20)
        text3, text_rect3 = render_text("Think about nothing, clear your mind", 20)
    text_surfs = cycle([text1, text2, text3])
    text_surf  = next(text_surfs)
    text_rects = cycle([text_rect1, text_rect2, text_rect3])
    text_rect  = next(text_rects)

    in1           = init_lsl("EEG", 0)
    i, trial_type = 0, 0
    done          = False
    TRIAL         = pygame.USEREVENT + 0
    pygame.time.set_timer(TRIAL, time_per)


    time, sample = read_lsl(in1)
    write_cal_trial(cal_file2, time, trial_type, mode)

    while (i < num_trials * 3) and not done:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if mode == 0 and event.type == SSVEP1:
                ssvep_surf1 = next(ssvep_surfs1)
            if mode == 0 and event.type == SSVEP2:
                ssvep_surf2 = next(ssvep_surfs2)
            if event.type == TRIAL:
                text_surf = next(text_surfs)
                text_rect = next(text_rects)
                trial_type += 1
                if trial_type == 3:
                    trial_type = 0
                write_cal_trial(cal_file2, time, trial_type, mode)

         screen.fill((0,0,0))
         screen.blit(text_surf, text_rect)
         if mode == 0:
              screen.blit(ssvep_surf1, (0, 0))
              screen.blit(ssvep_surf2, (SCREEN_WIDTH - 50, 0))

         pygame.display.flip()
         time, sample = read_lsl(in1)
         cal_file.write("%s %s \n" % (str(time), str(sample)))
         clock.tick(60)
        
def calibrate():
    f = open("./cal_file", "w")
    f2 = open("./cal_file_markers", "w")
    run_calibration_set(f, f2, 0, 1, 5000)
    run_calibration_set(f, f2, 1, 1, 5000)   
    f.close()
    f2.close()

def gameplay():
    all_sprites = pygame.sprite.Group()
    enemies     = pygame.sprite.Group()
    bullets     = pygame.sprite.Group()
    ship1       = ship()
    all_sprites.add(ship1)

    SPAWN      = pygame.USEREVENT + 0
    SPAWN_TIME = 2000
    pygame.time.set_timer(SPAWN, SPAWN_TIME)

    SSVEP1, ssvep_surfs1, ssvep_surf1 = generate_ssvep(1, 8)
    SSVEP2, ssvep_surfs2, ssvep_surf2 = generate_ssvep(2, 22)

    game_theme = pygame.mixer.music.load("../assets/game-theme-temp.mp3")
    pygame.mixer.music.play(-1, 0)

    in1        = init_lsl("EEG", 0)
    sample_buf = []
    buf_size   = 100
    CLASSIFY   = pygame.USEREVENT + 3
    pygame.time.set_timer(CLASSIFY, 300)

    score = 0
    score_frames = 0
    score_surf, score_rect = render_text("Score: %d" % score, 20)
    score_rect.top = SCREEN_HEIGHT - 20

    done = False
    pygame.key.set_repeat()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == SPAWN:
                e = enemy()
                enemies.add(e)
                all_sprites.add(e)
            if event.type == SSVEP1:
                ssvep_surf1 = next(ssvep_surfs1)
            if event.type == SSVEP2:
                ssvep_surf2 = next(ssvep_surfs2)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                b = bullet(ship1.angle)
                b.rect.x = ship1.rect.centerx
                b.rect.y = ship1.rect.centery
                all_sprites.add(b)
                bullets.add(b)
            if event.type == CLASSIFY:
                ssvep_result, mimg_result = classify_buf(sample_buf)
                if ssvep_result == 0:
                   ship1.rotate_ccw()
                if ssvep_result == 2:
                   ship1.rotate_cw()
                if mimg_result == 1:
                    b = bullet(ship1.angle)
                    b.rect.x = ship1.rect.centerx
                    b.rect.y = ship1.rect.centery
                    all_sprites.add(b)
                    bullets.add(b)


        all_sprites.update()

        player_hits = pygame.sprite.spritecollide(ship1, enemies, False, collided = pygame.sprite.collide_circle_ratio(0.7))
        if player_hits:
            leaderboard(score)
            done = True
        bullet_hits = pygame.sprite.groupcollide(enemies, bullets, True, True, pygame.sprite.collide_circle_ratio(0.7))
        score += len(bullet_hits) * 100

        screen.fill((0, 0, 0))
        screen.blit(ssvep_surf1, (0, 0))
        screen.blit(ssvep_surf2, (SCREEN_WIDTH - SSVEP_WIDTH, 0))
        if score_frames == 60:
            score += 1
            score_frames = 0
        else:
            score_frames += 1
        score_surf, _ = render_text("Score: %d" % score, 20)
        screen.blit(score_surf, score_rect)
        all_sprites.draw(screen)

        pygame.display.flip()

        time, sample = read_lsl(in1)
        sample_buf.append([time] + sample)
        sample_buf = sample_buf[-buf_size:]

        clock.tick(60)

def leaderboard(score):
    f = file.open("./high_scores", "w")

    names, name_rects = [], []
    i = 20
    for line in f.readline():
        name, name_rect = render_text("%s" % line, 20)
        name_rect.top
        names.append(name)
        name_rects.append(name_rect)
        i += 20

    prompt = "Enter your name: "

    while not done:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ENTER:
            done = True
        if event.type == pygame.KEYDOWN:
            prompt += pygame.key.name(event.key)

        screen.fill(( 0, 0, 0))
        prompt_surf, prompt_rect = render_text(prompt, 20)
        screen.blit(prompt_surf, prompt_rect)
        for idx, val in enumerate(names):
            screen.blit(val, name_rects[idx])
        
        pygame.display.flip()
        clock.tick(60)
    f.close()

def main():
    pygame.init()
    pygame.display.set_caption('Think-Blast')

    title_unscale   = pygame.image.load('../assets/title.png')
    title           = pygame.transform.scale(title_unscale, (500, 200))
    title_rect      = title.get_rect(center = (SCREEN_WIDTH/2, 150))

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

        play, play_rect = render_text("Press p to Play", 30)
        play_rect.top += 0
        cal, cal_rect   = render_text("Press c to Calibrate", 30)
        cal_rect.left = play_rect.left
        cal_rect.top += 40
        quit, quit_rect = render_text("Press q to Quit", 30)
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
