__author__ = 'JS'
import pygame


class Apple:
    #pos = [0, 0]
    #pos_0 = [0, 0]
    vel_y = 0
    ripe = 0

    # screen = []  # handle to pygame screen object
    # green_sprite = []  # green apple sprite
    # red_sprite = []  # red apple sprite
    # appleW = 0  # sprite width
    # appleH = 0  # sprite height

    def __init__(self, screen, sp1, sp2, x, y=0):
        self.pos = [x,y]
        self.pos_0 = [x,y]

        self.screen = screen
        self.green_sprite = sp1
        self.red_sprite = sp2
        self.appleW = sp1.get_rect().size[0]
        self.appleH = sp1.get_rect().size[1]

    def __str__(self):
        return str(self.pos)

    def getBoLePos(self):  # returns bottom left position
        return [self.pos[0], self.pos[1]+self.appleH]

    def getBoCePos(self):  # returns bottom center position
        return [self.pos[0]+self.appleW/2., self.pos[1]+self.appleH]

    def ripen(self, vel_y=5):
        if not self.ripe:
            self.ripe = 1
        else:
            self.ripe = 2
            self.vel_y = vel_y

    def reset(self):
        self.ripe = 0
        self.pos = self.pos_0[:]
        self.vel_y = 0

    def update(self):
        self.pos[1] += self.vel_y

    def render(self):
        if self.ripe > 0:
            image = self.red_sprite
        else:
            image = self.green_sprite
        self.screen.blit(image, [self.pos[0], self.pos[1]])
