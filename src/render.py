import pygame
from itertools import cycle

def ssvep(event_num, freq):
    """
    generate_ssvep() - creates SSVEP surfaces and timers
    event_num: The event number for the timer - must be unique.
    freq: The frequency of the SSVEP flashes.

    Helper function for rendering SSVEP flashes. SSVEP is rendered by switching
    between two surfaces when a certain timer event occurs.

    Return: The timer event, ssvep surfaces, current surfaces, and surface rect.
    """
    SSVEP = pygame.USEREVENT + event_num
    time  = int(round((1.0 / (freq * 2)) * 1000.0))
    pygame.time.set_timer(SSVEP, time)


    SSVEP_WIDTH  = 50
    SSVEP_HEIGHT = 50
    ssvep_on  = pygame.Surface((SSVEP_WIDTH, SSVEP_HEIGHT))
    ssvep_off = pygame.Surface((SSVEP_WIDTH, SSVEP_HEIGHT))
    ssvep_on.fill((255,255,255))
    ssvep_off.fill((0, 0, 0))

    ssvep_surfaces = cycle([ssvep_on, ssvep_off])
    ssvep_surface  = next(ssvep_surfaces)
    ssvep_rect     = ssvep_surface.get_rect()
    return SSVEP, ssvep_surfaces, ssvep_surface, ssvep_rect

def text(msg, size, xy_tuple):
    """
    render_text() - Render text in the default font.
    @msg:  The text to display.
    @size: The font size

    Helper function for rendering text.

    Return: The text object, and the centered text rect
    """
    select_font = pygame.font.Font("../assets/prstartk.ttf", size)
    text_surf   = select_font.render(msg, True, (255,255,255))
    text_rect   = text_surf.get_rect(center = (xy_tuple[0], xy_tuple[1]))
    return text_surf, text_rect

