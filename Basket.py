__author__ = 'JS'
import pygame


class Basket:
    # pos = [0, 0]
    vel_x = 0

    # screen = []  # handle to pygame screen object
    # front_sprite = []
    # back_sprite = []
    # glow_sprite = []
    # basketW = 0  # sprite width
    # basketH = 0  # sprite height
    maxSpeed = 0

    def __init__(self, screen, width, sp1, sp2, sp3, x, y, max_s):
        self.screen = screen
        self.width = width
        self.back_sprite = sp1
        self.front_sprite = sp2
        self.glow_sprite = sp3

        self.basketW = sp1.get_rect().size[0]
        self.basketH = sp1.get_rect().size[1]
        self.maxSpeed = max_s

        if self.is_valid_pos(x):
            self.pos = [x, y]
        else:
            self.pos = [self.width/2-self.basketW/2, y]

    def __str__(self):
        return str(self.pos)

    def getBoCePos(self):  # returns bottom center position
        return [self.pos[0]+self.basketW/2., self.pos[1]+self.basketH]

    def move(self, vel_x):
        self.vel_x = vel_x*self.maxSpeed

    def is_valid_pos(self, x):
        if 0 < x < self.width-self.basketW:
            return True
        else:
            return False

    def is_inside(self, pos):
        x = pos[0]
        y = pos[1]
        if y < self.pos[1]:
            # Object is too high = outside
            return 0
        elif self.pos[1] <= y < self.pos[1]+self.basketH*0.9:
            # is the object touching the basket's sides?
                # Object is "falling in"
            return 0
        else:
            if x < self.pos[0] or x > self.pos[0]+self.basketW:
                # Object fell outside basket boundary
                return -1
            else:
                # Object fell inside
                return 1

    def update(self):
        new_pos = self.pos[0] + self.vel_x
        if self.is_valid_pos(new_pos):
            self.pos[0] = new_pos

    def render(self, side='back'):
        if side == 'back':
            self.screen.blit(self.back_sprite, [self.pos[0], self.pos[1]])
        elif side == 'front':
            self.screen.blit(self.front_sprite, [self.pos[0], self.pos[1]])
        else:
            self.screen.blit(self.glow_sprite, [self.pos[0], self.pos[1]])

