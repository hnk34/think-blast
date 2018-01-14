import pygame
import math

class ship:
    def __init__(self):
        image = pygame.image.load('../assets/thinkblaster.png')
        self.simage = pygame.transform.scale(image,(100,100)) # scaled
        self.rimage = self.simage # scaled and rotated
        self.x = 350
        self.y = 350
        self.angle = 0 # in rad

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
