__author__ = 'JS'

import pygame
import random
import time
from math import floor
from threading import *

from OpenMenu import open_menu
from AppleTrial import AppleTrial

# Use "os" library to position the pygame window
import os
initWin_x = 10 #1400
initWin_y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (initWin_x, initWin_y)

# Auxiliary "find" function
def indices(values, func):
    return [i for (i, val) in enumerate(values) if func(val)]

# Auxiliary "sum" function between arrays, call with "map"
def add(x, y):
    return x+y

# Function: dist_joy
# Translates the joystick input based on the current disturbance
def dist_joy(axis, dist):
    if dist[0] == 2:
        # Slowed down
        return dist[1]*axis

    if dist[0] == 3:
        # Inverted axis
        return -axis

    if dist[0] == 4:
        # Freeze direction disturbance
        if dist[1] > 0:
            return -abs(axis)
        else:
            return abs(axis)

    if dist[0] == 5:
        # Freeze motion disturbance
        return 0

    # No disturbance
    return axis


# Pygame initialization
pygame.init()
pygame.font.init()
# clock = pygame.time.Clock()  # pygame clock

# Game window size
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
# width = 1200  # 1700
# height = 660  # 1000

# Game speed
gameFPS = 30.0  # 1200.0
basketSpeed = 300.0
fallSpeed = 125.0  # 4000.0

# Experiment condition
numTrials = 12  # number of times the apple will fall
# 1 - no disturbance 20%
# 2 - speed disturbance 20%
# 3 - inverse disturbance_change 20%
# 4 - inverse disturbance_nochange 20%
# 5 - stop disturbance 20%

# Initialize trial with set definitions
AT = AppleTrial(width, height, gameFPS, basketSpeed, fallSpeed, numTrials)

# Open splash screen menu
# om_res = open_menu()
# if om_res:
#     AT.start()
# else:
#     AT.exit_game = True
AT.start()

while not AT.exit_game:
    pygame.time.delay(40)

pygame.quit()
quit()

#################################################33

# global screen

eventTimer = -1  # timer to schedule events (ripe, fall, disturb)
eventSeq = 0  # index along event sequence
distDelay = 0.5  # time between beginning of apple fall and disturbance
distDur = 2.00  # time until disturbance ends
condDelay = 1.0

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255,125,0)

# this two can be moved into AppleTrial class
game_started = False
exit_game = False

# click_sound=pygame.mixer.Sound("laser5.ogg")

#################################################33


#################################################33



def playGame():
    global exit_game
    global game_started
    global Apples
    global eventTimer
    global eventSeq
    global RipeApple
    global ripeDelay
    global ripeBetween
    global screen
    global applesIn
    global applesOut
    global apples_fall
    global oTTimer

        # eventSeq += 1
        # elif eventSeq==1:
        #     time_till_dis = random.randrange(300,500)
        #     pygame.time.delay(time_till_dis)
        #     eventSeq+=1
        # elif eventSeq==2:
        #     # Start disturbance to basket motion
        #     if pick == 2:
        #     # Slow down
        #         basket.maxSpeed = 0.3*basketSpeed
        #     elif pick == 3:
        #         # invert axis
        #         basket.maxSpeed = -basketSpeed
        #         # eventTimer = time.time()+distDur  # set timer for next phase
        #         eventSeq += 1
        #     elif pick == 4:
        #         # invert axis with no change
        #         new_axis=change_direction(axis)
        #         basket.move(new_axis)
        #     elif pick == 5:
        #         basket.maxSpeed=0
        #     # subject begin to move
        #     eventSeq+=1
        # elif eventSeq == 3:
        #         # Finish disturbance (this should happen before the apple fell in/out)
        #         # basket.maxSpeed = basketSpeed
        #     eventTimer = -1
        #     eventSeq = 0
        # # Check if apples are inside the basket
        # for a in Apples:
        #     if a.ripe > 0:
        #         res = basket.is_inside(a.getBoLePos())
        #         # 0 = still falling
        #         # 1 = fell inside the basket
        #         # -1 = fell outside the basket
        #         if res != 0:
        #             # Apple fell
        #             if res == -1:
        #                 # Apple fell outside the basket
        #                 applesOut += 1
        #                 bpos = basket.getBoCePos()
        #                 apos = a.getBoCePos()
        #                 res_list.append(abs(bpos[0]-apos[0]))
        #             elif res == 1:
        #                 # Apple fell inside the basket
        #                 applesIn += 1
        #                 res_list.append(0)  # distance is 0
        #
        #             a.reset()  # reset apple back to tree
        #             trial += 1
        #             if trial >= numTrials:
        #                 # Game ends
        #                 game_started = False
        #                 #print applesIn, applesOut
        #                 #print dist_list
        #                 print res_list
        #                 openRes()
        #             else:
        #                 eventTimer = time.time() + ripeDelay  # set timer for new apple
        #                 basket.maxSpeed = basketSpeed


Open_Results= openRes()
if Open_Results:
   Open_Results.start()
else:
    Open_Results.exit_game = True

def startCallback():
    global game_started
    global exit_game
    game_started = True
    exit_game = False
    playGame()


def openRes():
    global exit_game
    global apples_fall
    menuScreen = pygame.display.set_mode(menuSize)  # Open window
    pygame.display.set_caption("Apple catching")

    #for theecuntingof differenes
    total=[]


    #set up font
    middle = 350
    spacing = 100
    resFont = pygame.font.SysFont('showcardgothic', 40)
    text =  basicFont.render('Results', True, ORANGE)
    text2 =  basicFont.render('Results', True, WHITE)
    menuScreen.fill(WHITE) #the background
    background=pygame.image.load('BG_tree.png').convert() #recommened to add convert
    start=pygame.image.load('start.png').convert_alpha()
    exit=pygame.image.load('exit.png').convert_alpha()
    basket_full=pygame.image.load('Basket_full.png').convert_alpha()
    basket_full= pygame.transform.scale(basket_full, (100, 100))
    basket_out=pygame.image.load('Basket_out.png').convert_alpha()
    basket_out= pygame.transform.scale(basket_out, (150, 120))

    menuScreen.blit(background,[0, 0])
    menuScreen.blit(text2, (357 - text2.get_width() // 2, 77 - text2.get_height() // 2))
    menuScreen.blit(text, (360 - text.get_width() // 2, 80 - text.get_height() // 2))

    text5 = resFont.render(str(applesIn),  True, WHITE)
    text6 = resFont.render(str(applesOut), True, WHITE)
    menuScreen.blit(text5, (middle - spacing -2 - text5.get_width() // 2, 180+10))
    menuScreen.blit(text6,(middle + spacing -2 - text6.get_width() // 2, 180+10))

    menuScreen.blit(basket_full, (middle - spacing - basket_full.get_width() // 2, 270+40 - basket_full.get_height() // 2))
    menuScreen.blit(basket_out, (middle + spacing - basket_out.get_width() // 2, 280+40 - basket_out.get_height() // 2))
    menuScreen.blit(start,[550,420])
    menuScreen.blit(exit,[50, 420])

    text3b = resFont.render('In',  True, BLACK)
    text4b = resFont.render('Out', True, BLACK)
    menuScreen.blit(text3b, (middle - spacing - text3b.get_width() // 2, 340+70))
    menuScreen.blit(text4b,(middle + spacing - text4b.get_width() // 2, 340+70))

    # # calculating the percentage of each deltas (for 1 to 9)
    neg_apples_fall=[i * -1 for i in apples_fall]
    diff = map(add , apples_fall[0:len(apples_fall)-1], neg_apples_fall[1:len(neg_apples_fall)])
    diff_abs= [abs(i) for i in diff]

    # for t in range(1,10):
    #     count = [abs(i) == t for i in diff]
    #     total.append(sum(count))
    # total_per=[i*100/sum(total) for i in total]

    # calculating the percentage of each deltas (for 1 to 9) regarding each case (1 till 4) individually
    new_dist_list=dist_list[1:len(dist_list)]
    # list_num1=indices(range(0,new_dist_list), lambda x: x==1)
    # list_num2=indices(range(0,new_dist_list), lambda x: x==2)
    # list_num3=indices(range(0,new_dist_list), lambda x: x==3)
    # list_num4=indices(range(0,new_dist_list), lambda x: x==4)
    def percent_delta(p,diff_abs,new_dist_list):
        total=[]
        list_num= indices(range(0,len(new_dist_list)), lambda x: x==p)
        for num in list_num:
            total.append(diff_abs[num])
        for t in range(1,10):
            count = [i==t for i in total]
            total.append(sum(count))
        total_per=[i*100/sum(total) for i in total]
        print total_per

    for p in range(1,5):
        percent_delta(p,diff_abs,new_dist_list)

    # print total
    # print total_per

    pygame.display.update()

    # Connect the joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            # if event.type is pygame.JOYAXISMOTION:
            #     axis = joystick.get_axis(0)
            #     if axis>0.5:
            #         startCallback()
            if event.type is pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    exit_game = True
                if event.key == pygame.K_RIGHT:
                    startCallback()
        # clock.tick(gameFPS) # the number in the () is the number of frame per sec


pygame.quit()
quit()


