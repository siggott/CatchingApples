__author__ = 'SJ'
import pygame
import random
from math import floor
import threading
import time

from Apple import Apple
from Basket import Basket


class AppleTrial:
    def __init__(self, w=1700, h=1000, gameFPS=50.0, basketSpeed=7000.0, appleFallSpeed=4000.0, numTrials=100):
        # Game window size
        self.width = w
        self.height = h
        self.size = (w, h)

        # Game speed
        self.FPS = gameFPS
        self.basketSpeed = basketSpeed/gameFPS
        self.appleFallSpeed = appleFallSpeed/gameFPS

        # Apple fall variables
        self.nApples = 10
        self.ripeDelay = 0  # time between turning red and falling (in ms)
        self.ripeBetween = 0  # time until next apple ripens (from fall/catch, in ms)

        # Experiment condition
        self.numTrials = numTrials  # number of times the apple will fall
        self.trial_i = 0

        dist_dist = [1./4., 1./4., 1./8., 1./8., 1./4.]  # distribution of disturbances
        # 1 - no disturbance 25%
        # 2 - speed disturbance 25%
        # 3 - inverse disturbance with correction 12.5%
        # 4 - inverse disturbance with no correction 12.5%
        # 5 - freeze disturbance (remaining % = 25%)
        no_dis = int(floor(numTrials*dist_dist[0]))
        with_dis_op_corr = int(floor(numTrials*dist_dist[1]))
        with_dis_op_nocorr = int(floor(numTrials*dist_dist[2]))
        with_dis_speed = int(floor(numTrials*dist_dist[3]))
        with_dis_stop = numTrials - no_dis - with_dis_op_corr - with_dis_op_nocorr - with_dis_speed

        # Initialize list of disturbances for trial run
        self.dist_list_i = 0  # current position on dist list
        self.dist_list = [1 for i in range(no_dis)]+[2 for j in range(with_dis_speed)] + \
            [3 for k in range(with_dis_op_corr)]+[4 for k in range(with_dis_op_nocorr)]+\
            [5 for k in range(with_dis_stop)]
        random.shuffle(self.dist_list)  # shuffle disturbance order
        # print dist_list

        # Initialize distribution of speed disturbance
        Speeds = [0.3, 0.5, 0.7]
        speed_dist = [1., 0., 0.]  # distribution of disturbances
        Nspeed1 = int(floor(with_dis_speed*speed_dist[0]))
        Nspeed2 = int(floor(with_dis_speed*speed_dist[1]))
        Nspeed3 = with_dis_speed - Nspeed1 - Nspeed2

        self.speed_list_i = 0  # current position on speed list
        self.speed_list = [Speeds[0] for i in range(Nspeed1)] + [Speeds[1] for i in range(Nspeed2)] + \
            [Speeds[2] for i in range(Nspeed3)]
        random.shuffle(self.speed_list)  # shuffle disturbance order

        # Reset trial results
        self.applesIn = 0
        self.applesOut = 0
        self.res_list = []  # stores distance of apple from basket (0 when success)
        self.apples_fall = []  # stores the order in which the apples fell

        self.frame_count = 0
        self.run_time = 0
        self.basket_pos = []  # stores the basket's position at every pygame update

        # Initialize attributes loaded by "start" method
        # Sprites
        self.background = []
        self.sred_apple = []
        self.sgreen_apple = []
        self.sbasket_im_bk = []
        self.sbasket_im_fr = []
        self.sbasket_im_gl = []
        # Objects (basket and apples)
        self.basket = []
        self.basket_glow = 0
        self.ApplePos = []
        self.Apples = []
        self.RipeApple = []
        # Screen + joystick
        self.screen = []
        self.joystick = []
        self.j_axis = 0  # set joystick to 0
        # Threads
        self.u_and_r_thread = []
        # self.input_thread = []  # pygame did not like releasing events on a thread
        self.trial_thread = []
        self.ripe_event = threading.Event()

        # Initialize "exit game" flag
        self.exit_game = False

        # Initialize pygame clock
        self.clock = pygame.time.Clock()


    def start(self):
        # Start empty pygame window (to load sprites)
        self.screen = pygame.display.set_mode((1,1),pygame.NOFRAME)

        # Load graphics
        background = pygame.image.load('TreeShort_clean.png').convert_alpha()
        red_apple = pygame.image.load('red_apple.png').convert_alpha()
        green_apple=pygame.image.load('green_apple.png').convert_alpha()
        basket_im_bk=pygame.image.load('BasketBack.png')
        basket_im_fr=pygame.image.load('BasketFront.png')
        basket_im_gl=pygame.image.load('BasketGlow.png')

        # Scale graphics
        self.background = pygame.transform.scale(background, (self.width, self.height))
        self.sred_apple = pygame.transform.scale(red_apple, (75, 75))  # smaller red apple
        self.sgreen_apple = pygame.transform.scale(green_apple, (75, 75))  # smaller green apple
        self.sbasket_im_bk = pygame.transform.scale(basket_im_bk, (199, 199))  # smaller basket back
        self.sbasket_im_fr = pygame.transform.scale(basket_im_fr, (199, 199))  # smaller basket front
        self.sbasket_im_gl = pygame.transform.scale(basket_im_gl, (199, 199))  # smaller basket glow

        # Initialize game elements
        self.basket = Basket(self.screen, self.width,                    # screen + screen width
            self.sbasket_im_bk, self.sbasket_im_fr, self.sbasket_im_gl,  # sprites
            -1, self.height*0.68, self.basketSpeed)                       # x, y, speed

        padding = self.width/15.
        # appleW = self.sgreen_apple.get_rect().size[0]
        self.ApplePos = [padding+i*(self.width-2*padding)/self.nApples for i in range(self.nApples)]
        self.Apples = [Apple(self.screen, self.sgreen_apple, self.sred_apple,
                             self.ApplePos[i], self.height*0.23) for i in range(self.nApples)]
        self.RipeApple = -1  # Current apple falling (-1, no apple falling)
        # print dist_Apples

        ########### end of graphics loading + element loading #########

        # Open game window
        self.screen = pygame.display.set_mode(self.size,pygame.FULLSCREEN)

        # Connect the joystick
        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except:
            print "No joystick found, use key arrows"

        # self.update_and_render()
        self.u_and_r_thread = threading.Thread(None,self.update_and_render,'u_and_r_thread')
        self.trial_thread = threading.Thread(None,self.run_trial,'trial_thread')
        self.run_time = time.time()
        self.ripe_event.set()  # allow first apple to ripen
        self.u_and_r_thread.start()  # start update+render thread
        self.trial_thread.start()  # start trial thread

        self.check_input() # start checking input

    def update_and_render(self):
        while not self.exit_game:
            # print "Thread 1 live"
            # Move basket based on joystick input
            self.basket.move(self.j_axis)

            # Render all the game elements
            self.screen.fill((255.0, 255.0, 255.0))  # the background
            self.screen.blit(self.background, [0, 0])  # tree
            self.basket.update()
            if self.basket_glow > 0:
                self.basket_glow -= 1
                self.basket.render('glow')
            else:
                self.basket.render('back')

            for a in self.Apples:
                a.update()
                a.render()
            self.basket.render('front')

            pygame.display.update()
            self.is_in()
            self.clock.tick(self.FPS)  # the number in the () is the number of frame per sec

            self.frame_count += 1
            self.basket_pos.append(self.basket.pos[0])

    def check_input(self):
        while not self.exit_game:
            # Take care of input events
            # print "Thread 2 live"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True
                if event.type is pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_game = True
                    # if event.key == pygame.K_LEFT:
                    #     self.exit_game = True
                    if event.key == pygame.K_LEFT:
                        self.j_axis = -1
                    elif event.key == pygame.K_RIGHT:
                        self.j_axis = 1
                if event.type == pygame.KEYUP: #key released
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.j_axis = 0 #it doesnt change anymore
                if event.type is pygame.JOYAXISMOTION:
                    # if game_started:
                    #     self.axis = self.joystick.get_axis(0)
                    self.j_axis = self.joystick.get_axis(0)

    def run_trial(self):
        while not self.exit_game:
            # print "Trial thread is live"
            self.ripe_event.wait()  # wait until allowed to ripen the next apple
            self.ripe_event.clear()

            # Pick the next apple to become ripe
            self.pick_next_apple()

            self.apples_fall.append(self.RipeApple)  # Add the pick to the list of apples that fell
            self.Apples[self.RipeApple].ripen()  # Apple becomes red
            # Possibly add a delay between becoming red and falling
            self.Apples[self.RipeApple].ripen(self.appleFallSpeed) # Apple starts falling

    @staticmethod
    def indices(values, func):
        return [i for (i, val) in enumerate(values) if func(val)]

    # Compare desired apple to distance from last apple (by index)
    def apples_right_of_a(self, x):
        return 7 + self.RipeApple > x > 4 + self.RipeApple

    def apples_left_of_a(self, x):
        return self.RipeApple - 7 < x < self.RipeApple - 4

    # Compare desired position of next apple to distance from basket
    @staticmethod
    def apples_right_of_b(x, basket_i):
        return 7 + basket_i >= x >= 4 + basket_i

    @staticmethod
    def apples_left_of_b(x, basket_i):
        return basket_i - 7 <= x <= basket_i - 4

    def pick_next_apple(self):
        pick = self.dist_list[self.trial_i]
        pick_by_pos = self.basket.pos[0]  # pick next apple based on basket position
        # pick_by_pos = self.RipeApple  # pick next apple based on last apple position

        # Calculate apple index based on basket position
        basket_inds = self.indices(self.ApplePos, lambda x: x > self.basket.pos[0])
        if not basket_inds:
            # basket is to the right
            basket_i = self.nApples-1
        else:
            if basket_inds[0] == 0:
                # basket is to the left
                basket_i = 0
            else:
                # find the closest apple between 2
                if self.ApplePos[basket_inds[0]]-self.basket.pos[0] > \
                        self.basket.pos[0]-self.ApplePos[basket_inds[0]-1]:
                    basket_i = basket_inds[0]-1
                else:
                    basket_i = basket_inds[0]

        # if not self.RipeApple or pick == 5:
        #     # If this is the first apple or there's a "freezing" disturbance, pick a random apple
        #     # self.RipeApple = random.randrange(0, self.nApples)
        # else:
        if pick == 2:
            # Lower speed disturbance, pick apples far away from the basket
            MaxDeltaX = 0.3*self.basketSpeed/self.appleFallSpeed*(self.basket.pos[1]-self.Apples[0].pos_0[1])
            des_pos_right = pick_by_pos + MaxDeltaX
            des_pos_left = pick_by_pos - MaxDeltaX

            # select riped apple according to the basket location
            inds_right = self.indices(self.ApplePos, lambda x: x > des_pos_right)
            inds_left = self.indices(self.ApplePos, lambda x: x < des_pos_left)

            pos_inds = []  # Possible apples to ripen
            if len(inds_right) > 0:
                pos_inds.append(inds_right[0])  # first apple out of range
                pos_inds.append(inds_right[0]-1)  # last apple in range
            if len(inds_left) > 0:
                pos_inds.append(inds_left[-1])  # first apple out of range
                pos_inds.append(inds_left[-1]+1) # last apple in range

            if not pos_inds:
                # If no possible apples were found, pick apples that are a certain distance from the last ripe apple
                inx_right = self.indices(range(0,self.nApples), lambda x: self.apples_right_of_b(x, basket_i))
                inx_left = self.indices(range(0,self.nApples), lambda x: self.apples_left_of_b(x, basket_i))
                choices = inx_right+inx_left
            else:
                choices = pos_inds
                # Apples[RipeApple].ripen()  # ripen (apple becomes red)
                # click_sound.play()  # play falling sound
        else:  # pick==1,3,4
            # If there's no disturbance or direction change disturbance (with/without correction),
            # pick apples that are a certain distance from the last ripe apple
            inx_right = self.indices(range(0,self.nApples), lambda x: self.apples_right_of_b(x, basket_i))
            inx_left = self.indices(range(0,self.nApples), lambda x: self.apples_left_of_b(x, basket_i))
            choices = inx_right+inx_left

        # choices = [x for x in choices if x != self.RipeApple]
        self.RipeApple = random.choice(choices)  # Select random apple from possible indices

    def is_in(self):
        for a in self.Apples:
            if a.ripe > 0:
                res = self.basket.is_inside(a.getBoLePos())
                # 0 = still falling
                # 1 = fell inside the basket
                # -1 = fell outside the basket
                # Apple fell
                if res == 0:
                    continue

                if res == -1:
                    # Apple fell outside the basket
                    self.applesOut += 1
                    bpos = self.basket.getBoCePos()
                    apos = a.getBoCePos()
                    self.res_list.append(abs(bpos[0]-apos[0]))
                elif res == 1:
                    # Apple fell inside the basket
                    self.applesIn += 1
                    self.res_list.append(0)  # distance is 0
                    self.basket_glow = int(0.3*self.FPS)

                a.reset()  # reset apple back to tree

                self.trial_i += 1

                if self.trial_i >= self.numTrials:
                    # Game ends
                    # game_started = False
                    self.exit_game = True
                    self.run_time = time.time() - self.run_time
                    print self.run_time
                    print self.frame_count

                    print self.basket_pos
                else:
                    # eventTimer = time.time() + ripeDelay  # set timer for new apple
                    self.ripe_event.set()
                    self.basket.maxSpeed = self.basketSpeed