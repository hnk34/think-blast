import pygame
import math
import random

SCREEN_HEIGHT = 700
SCREEN_WIDTH  = 1024
screen        = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect   = screen.get_rect()
OOB_HEIGHT    = 1200
OOB_WIDTH     = 900
bounds        = pygame.display.set_mode((OOB_WIDTH, OOB_HEIGHT))
bounds_rect   = bounds.get_rect()
bounds_rect.top  -= 150
bounds_rect.left -= 150

class game_object(pygame.sprite.Sprite):
    def __init__(self, angle):
        super(game_object, self).__init__()
        self.angle = angle
        self.speed = 0

    def move_forward(self):
        self.rect.move_ip(-self.speed*math.sin(self.angle), -self.speed*math.cos(self.angle))

    def update(self):
        self.move_forward()
        if not bounds_rect.contains(self.rect):
            self.kill()

class ship(game_object):
    def __init__(self):
        super(ship, self).__init__(0)
        image          = pygame.image.load('../assets/thinkblaster.png')
        self.image     = pygame.transform.scale(image,(50,50))
        self.rect      = self.image.get_rect()
        self.rect.left = SCREEN_WIDTH / 2
        self.rect.top  = SCREEN_HEIGHT / 2
        self.oimage    = self.image
        self.speed     = 2
        self.cw_counter, self.ccw_counter = 0, 0

    def move_forward(self):
        self.rect.move_ip(-self.speed*math.sin(self.angle), -self.speed*math.cos(self.angle))
        self.rect.clamp_ip(screen_rect)

    def move_backward(self):
        self.rect.move_ip(round(self.speed*math.sin(self.angle)), round(self.speed*math.cos(self.angle)))
        self.rect.clamp_ip(screen_rect)

    def rotate_cw(self):
        self.angle -= (math.pi/4)
        round_angle =  int(45 * round(math.degrees(self.angle/45)))
        self.image = pygame.transform.rotate(self.oimage, round_angle)
        self.rect  = self.image.get_rect(center = self.rect.center)

    def rotate_ccw(self):
        self.angle += (math.pi/4)
        round_angle = int(45 * round(math.degrees(self.angle/45)))
        self.image = pygame.transform.rotate(self.oimage, round_angle)
        self.rect  = self.image.get_rect(center = self.rect.center)

    def update(self):
        pressed = pygame.key.get_pressed()
        # The counter variables are meant to force a 5-frame delay after rotation
        # key input, to prevent unwanted keystrokes.
        if pressed[pygame.K_LEFT] and self.ccw_counter == 0:
            self.rotate_ccw()
            self.ccw_counter += 5
        else:
            if self.ccw_counter > 0:
                self.ccw_counter -= 1
        if pressed[pygame.K_RIGHT] and self.cw_counter == 0:
            self.rotate_cw()
            self.cw_counter += 5
        else:
            if self.cw_counter > 0:
                self.cw_counter -= 1
        if pressed[pygame.K_UP]: 
            self.move_forward()
        if pressed[pygame.K_DOWN]:
            self.move_backward()

class enemy(game_object):
    def __init__(self):
        super(enemy, self).__init__(0)
        image = pygame.image.load('../assets/enemy.png')
        self.speed = 2       
 
        self.size = random.randint(0,2)
        if self.size == 0: # small enemy
            self.image = pygame.transform.scale(image, (50, 50))
        if self.size == 1: # medium
            self.image = pygame.transform.scale(image, (100, 100))
        if self.size == 2: # large
            self.image = pygame.transform.scale(image, (150, 150))

        self.rect      = self.image.get_rect()
        self.rect.left = random.random() * SCREEN_WIDTH - self.rect.width
        
        spawn_top = random.choice([True, False])
        if spawn_top:
            self.rect.top = 0
            self.angle    = random.choice([math.pi, math.pi+(math.pi/4), math.pi-(math.pi/4)])
        else:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
            self.angle    = random.choice([0, math.pi/4, (2*math.pi)-(math.pi/4)])

class bullet(game_object):
    def __init__(self, angle):
        super(bullet, self).__init__(angle)
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 0))
        self.rect  = self.image.get_rect()
        self.speed = 5
