import pygame
import high_scores
import interface
import render
import numpy
from game_object import ship, enemy, bullet

def gameplay(screen, clock):
    all_sprites = pygame.sprite.Group()
    enemies     = pygame.sprite.Group()
    bullets     = pygame.sprite.Group()
    ship1       = ship()
    all_sprites.add(ship1)

    clf = interface.get_classifier("./cal_ssvep.csv")
    print "Classifier generated!"
    f = interface.trial_to_feat(x)
    clf.classify_buf()

    SPAWN      = pygame.USEREVENT + 0
    SPAWN_TIME = 2000
    pygame.time.set_timer(SPAWN, SPAWN_TIME)

    SSVEP1, ssvep_surfs1, ssvep_surf1, ssvep_rect1 = render.ssvep(1, 8.0)
    SSVEP2, ssvep_surfs2, ssvep_surf2, ssvep_rect2 = render.ssvep(2, 22.0)

    game_theme = pygame.mixer.music.load("../assets/game-theme-temp.mp3")
    pygame.mixer.music.play(-1, 0)

    CLASSIFY   = pygame.USEREVENT + 3
    pygame.time.set_timer(CLASSIFY, 1000)

    screen_rect = screen.get_rect()
    score = 0
    score_frames = 0
    score_surf, score_rect = render.text("Score: %d" % score, 20, screen_rect.center)
    score_rect.top = SCREEN_HEIGHT - 40

    inlet = interface.init_lsl(0)

    i = 0
    sample_buf = numpy.empty(60)
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

        all_sprites.update()
        player_hits = pygame.sprite.spritecollide(ship1, enemies, False, pygame.sprite.collide_circle_ratio(0.7))
        if player_hits:
            high_scores(score)
            done = True
        bullet_hits = pygame.sprite.groupcollide(enemies, bullets, True, True, pygame.sprite.collide_circle_ratio(0.7))
        score += len(bullet_hits) * 100

        ssvep_rect1.top = ship1.rect.top
        ssvep_rect1.left = ship1.rect.left - 160
        ssvep_rect2.top  = ship1.rect.top     
        ssvep_rect2.left = ship1.rect.left + 175

        screen.fill((0, 0, 0))
        screen.blit(ssvep_surf1, ssvep_rect1)
        screen.blit(ssvep_surf2, ssvep_rect2)
        if score_frames == 60:
            score += 1
            score_frames = 0
        else:
            score_frames += 1
        score_surf, _ = render.text("Score: %d" % score, 20, (0,0))
        screen.blit(score_surf, score_rect)
        all_sprites.draw(screen)

        pygame.display.flip()

        times, samples = interface.read_lsl(inlet)
        for s in samples:
            sample_buf[i] = numpy_asarray(sample[0:8])
            i+= 1
        if i >= 245:
            ssvep_result, _ = classify_buf(clf, sample_buf)
            if ssvep_result == 0:
               ship1.rotate_ccw()
            if ssvep_result == 2:
               ship1.rotate_cw()
            i = 0
            sample_buf = numpy.empty([250,8])

        clock.tick(60)

