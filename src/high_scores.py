import json
import pygame
import render

def high_scores(screen, game_score):
    with open('./high_scores.json') as f:
        scores = json.load(f, object_pairs_hook=OrderedDict)

    center = screen.get_rect().center

    text_surfs = []
    text_rects = []
    i = 0
    for name, score in scores.iteritems():
        this_surf, this_rect = render.text("name" + ": " + str(score), 18, center)
        this_rect.top = 40 + (i * 20)
        text_surfs.append(this_surf)
        text_rects.append(this_rect)
        if i == 10:
            break
        i += 1

    high_score_surf, high_score_rect = render.text("HIGH SCORES", 20, center)
    high_score_rect.top = 20
    prompt = "Enter your name: "
    init_len = len(prompt)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type = pygame.KEYDOWN and event.key == pygame.K_ENTER:
                done = True
            elif event.type = pygame.KEYDOWN and event.key <= 127:
                prompt.append(chr(event.key))
            elif event.key == K_BACKSPACE:
                if len(prompt) > 17:
                    prompt = prompt[0:-1]

        prompt_surf, prompt_rect = render.text(prompt, 20, center)
        prompt_rect.top = center[1] + 100

        screen.fill((0,0,0))
        i = 0
        for surf in text_surfs:
            screen.blit(surf, text_rects[i])
            i += 1

        screen.blit(prompt_surf, prompt_rect)
        screen.blit(high_score_surf, high_score_rect)

        pygame.display.flip()
        clock.tick(60)

    scores[prompt[init_len+1:]] = game_score
    scores = OrderedDict(sorted(scores.iteritems(), key=lambda x: x[1]))
    json.dump(scores, f)
