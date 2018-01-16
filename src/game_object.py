import pygame
import math
import random

SCREEN_HEIGHT = 700
SCREEN_WIDTH  = 600
screen        = pygame.display.set_mode((SCREEN_WIDTH + 100, SCREEN_HEIGHT))
screen_rect   = screen.get_rect()

class game_object(pygame.sprite.Sprite):
    def __init__(self, angle):
        super(game_object, self).__init__()
        self.angle = angle

class ship(game_object):
    def __init__(self):
        super(ship, self).__init__(0)
        image          = pygame.image.load('../assets/thinkblaster.png')
        self.image     = pygame.transform.scale(image,(50,50))
        self.rect      = self.image.get_rect()
        self.rect.left = SCREEN_WIDTH / 2
        self.rect.top  = SCREEN_HEIGHT / 2
        self.oimage    = self.image

    def move_forward(self):
        self.rect.move_ip(-1*math.sin(self.angle), -1*math.cos(self.angle))
        self.rect.clamp_ip(screen_rect)

    def move_backward(self):
        self.rect.move_ip(1*math.sin(self.angle), 1*math.cos(self.angle))
        self.rect.clamp_ip(screen_rect)

    def rotate_cw(self):
        self.angle += 0.2
        if self.angle >= 6.23:
            self.angle -= 6.23
        self.image = pygame.transform.rotate(self.oimage, math.degrees(self.angle))
        self.rect  = self.image.get_rect(center = self.rect.center)

    def rotate_ccw(self):
        self.angle -= 0.2
        if self.angle <= 0:
            self.angle += 6.23
        self.image = pygame.transform.rotate(self.oimage, math.degrees(self.angle))
        self.rect  = self.image.get_rect(center = self.rect.center)

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: 
            self.move_forward()
        if pressed[pygame.K_DOWN]:
            self.move_backward()
        if pressed[pygame.K_LEFT]: 
            self.rotate_ccw()
        if pressed[pygame.K_RIGHT]:
            self.rotate_cw()

class enemy(game_object):
    def __init__(self):
        super(enemy, self).__init__(0)
        image = pygame.image.load('../assets/enemy.png')
        
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
            self.angle    = (math.pi/2) + (random.random()*math.pi)
        else:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
            self.angle    = (3*math.pi)/2 + (random.random()*math.pi)

    def update(self):
        self.move_forward()
        if not screen_rect.contains(self.rect):
            self.kill()

    def move_forward(self):
        self.rect.move_ip(-1*math.sin(self.angle), -1*math.cos(self.angle))
