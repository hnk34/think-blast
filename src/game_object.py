import pygame
import math
import random

screen      = pygame.display.set_mode((700,700))
screen_rect = screen.get_rect()

class game_object(pygame.sprite.Sprite):
    def __init__(self, angle):
        super(game_object, self).__init__()
        self.angle = angle

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
        # figure out how to rotate without skew

    def rotate_ccw(self):
        self.angle -= 0.2
        if self.angle < 6.23:
            self.angle += 6.23

class ship(game_object):
    def __init__(self):
        super(ship, self).__init__(0)
        image          = pygame.image.load('../assets/thinkblaster.png')
        self.image     = pygame.transform.scale(image,(50,50))
        self.rect      = self.image.get_rect()
        self.rect.left = 350
        self.rect.top  = 350
        self.rimage    = self.image

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
    def __init__(self, spawn_top):
        super(enemy, self).__init__(0)
        image     = pygame.image.load('../assets/enemy.png')
        
        self.size = random.randint(0,2)
        if self.size == 0: # small enemy
            self.image = pygame.transform.scale(image, (50, 50))
        if self.size == 1: # medium
            self.image = pygame.transform.scale(image, (100, 100))
        if self.size == 2: # large
            self.image = pygame.transform.scale(image, (150, 150))

        self.rect      = self.image.get_rect()
        self.rect.left = random.random() * 700
        self.rect.top  = random.choice([50, 650])

    def update(self):
        self.move_forward()
