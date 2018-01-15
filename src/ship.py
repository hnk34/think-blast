import pygame
import math
import random

class game_object(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super(game_object, self).__init__()
        self.x = x
        self.y = y 
        self.angle = angle

    def move_forward(self):
        self.x -= math.sin(self.angle)
        self.y -= math.cos(self.angle)
        if self.x >= 650:
            self.x = 650
        if self.x <= 0:
            self.x = 0

    def move_backward(self):
        self.x += math.sin(self.angle)
        self.y += math.cos(self.angle)
        if self.x >= 650:
            self.x = 650
        if self.x <= 0:
            self.x = 0

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
    def __init__(self, x, y, angle):
        super(ship, self).__init__(x, y, angle)
        image = pygame.image.load('../assets/thinkblaster.png')
        self.simage = pygame.transform.scale(image,(100,100)) # scaled
        self.rimage = self.simage # scaled and rotated

    def keyboard_movement(self):
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
    def __init__(self, size):
        super(enemy, self).__init__(x, y, angle)
        image = pygame.game.load('../assets/enemy.png')
        if size == 0: # small enemy
            self.simage = pygame.transform.scale(image, (50, 50))
        if size == 1: # medium
            self.simage = pygame.transform.scale(image, (100, 100))
        if size == 2: # large
            self.simage = pygame.transform.scale(image, (150, 150))
        self.rimage = self.simage
