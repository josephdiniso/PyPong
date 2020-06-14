#!/usr/bin/env python3

import random
import math
import pickle

import pygame
import winsound
import threading

from socket_client import SocketClient

class game_env:
    def __init__(self):
        #Color initializations
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.BALL_COLOR = (255,255,255)        
        
        #Pygame initializations
        pygame.init()
        pygame.mixer.init(22050, -8, 16, 65536 )
        self.size = (500,500)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("PyPong")

        #Block position initializations
        self.left_y = self.size[1]/2
        self.right_y = self.size[1]/2
        self.pos_dict = {0:self.left_y, 1:self.right_y}
        self.block_size = 50

        #Block movement booleans
        self.left_down = False
        self.right_down = False
        self.left_up = False
        self.right_up = False

        #Ball velocity variables
        self.ball_xv = 6
        self.ball_yv = 6
        self.ball_x = self.size[0]/2
        self.ball_y = self.size[1]/2
        self.abs_vel = 4
        self.ball_time = 0
        self.flip = 0

        #Side Score Variables
        self.side_score = {0: 0, 1: 0}

        #Text Variables
        self.font = pygame.font.Font('freesansbold.ttf', 15) 
        
        self.socket = SocketClient(self.pos_dict[0], self.pos_dict[1])
        threading.Thread(target=self.comm).start()
        done = False
        self.ballInit()
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.left_down = True
                    elif event.key == pygame.K_DOWN:
                        self.right_down = True
                    elif event.key == pygame.K_w:
                        self.left_up = True
                    elif event.key == pygame.K_UP:
                        self.right_up = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_s:
                        self.left_down = False
                    elif event.key == pygame.K_DOWN:
                        self.right_down = False
                    elif event.key == pygame.K_w:
                        self.left_up = False
                    elif event.key == pygame.K_UP:
                        self.right_up = False
            self.screen.fill(self.BLACK)
            self.checkMovement()
            self.drawBlocks()
            self.drawBall()
            self.checkColl()
            if self.socket.left:
                self.ballMove()
            self.clock.tick(120)
            pygame.display.flip()
        pygame.quit()


    def comm(self):
        while 1:
            if self.socket.left:
                self.socket.pos_left = self.pos_dict[0]
                self.pos_dict[1] = self.socket.pos_right
                self.socket.ball_x = self.ball_x
                self.socket.ball_y = self.ball_y
            else:
                self.socket.pos_right = self.pos_dict[1]
                self.pos_dict[0] = self.socket.pos_left
                self.ball_x = self.socket.ball_x
                self.ball_y = self.socket.ball_y

    def checkMovement(self):
        if self.left_down:
            self.down(0)
        if self.right_down:
            self.down(1)
        if self.left_up:
            self.up(0)
        if self.right_up:
            self.up(1)

    def down(self, side):
        if not self.pos_dict[side] + self.block_size >= self.size[1]:
            self.pos_dict[side] += 5
    
    def up(self, side):
        if not self.pos_dict[side] - self.block_size <= 0:
            self.pos_dict[side] -= 5

    
    def drawBlocks(self):
        pygame.draw.rect(self.screen, self.WHITE, [0, self.pos_dict[0]-self.block_size, 20, 2*self.block_size])
        pygame.draw.rect(self.screen, self.WHITE, [self.size[0]-20, self.pos_dict[1]-self.block_size, 20, 2*self.block_size])
    
   
    def drawBall(self):
        pygame.draw.circle(self.screen, self.BALL_COLOR, (self.ball_x, self.ball_y), 10)
    
   
    def ballInit(self):
        direction_x = [-1,1][random.randrange(2)]
        direction_y = [-1,1][random.randrange(2)]
        rand_num = random.randint(6,8)
        self.ball_xv*=direction_x*rand_num
        self.ball_yv*=direction_y*rand_num

   
    def ballMove(self):
        if pygame.time.get_ticks() - self.ball_time > self.abs_vel:
            self.ball_x += int(self.ball_xv)
            self.ball_y += int(self.ball_yv)
            self.ball_time = pygame.time.get_ticks()
            #print(str(self.ball_xv)+","+str(self.ball_yv))

    
    def checkColl(self):
        if pygame.time.get_ticks() - self.flip > 30:
            if self.ball_y-10 <= 0 or self.ball_y+10 >= self.size[1]:
                self.ball_yv *= -1
            if (self.ball_x-10 <= 20 and self.ball_x-10 >= 0) and (self.ball_y+10 >= self.pos_dict[0]-self.block_size and self.ball_y-10 <= self.pos_dict[0]+self.block_size):
                self.ballColl(0)
            elif (self.ball_x+10 >= self.size[0]-20 and self.ball_x+10 <= self.size[0]) and (self.ball_y+10 >= self.pos_dict[1]-self.block_size and self.ball_y-10 <= self.pos_dict[1]+self.block_size):
                self.ballColl(1)
            elif self.ball_x-15 < 0:
                self.round_over(1)
            elif self.ball_x+15 > self.size[0]:
                self.round_over(0)
            self.flip = pygame.time.get_ticks()
        
    
    def ballColl(self, side):
        if self.ball_y < self.pos_dict[side]:
            #abs_vel = math.sqrt(self.ball_xv**2+self.ball_yv**2)
            m = -75/(self.block_size)
            angle = m * abs(self.ball_y-self.pos_dict[side])
            self.ball_yv = -round(4 * math.sin(angle))
            self.ball_xv = round(4 * math.cos(angle))

        elif self.ball_y >= self.pos_dict[side]:
            #abs_vel = math.sqrt(self.ball_xv**2+self.ball_yv**2)
            m = -75/(self.block_size)
            angle = m * abs(self.ball_y-self.pos_dict[side])
            self.ball_yv = round(6 * math.sin(angle))
            self.ball_xv = round(6 * math.cos(angle))
        
        if side == 1:
            self.ball_xv = abs(self.ball_xv) * -1
        else:
            self.ball_xv = abs(self.ball_xv)

        if self.abs_vel > 0:
            self.abs_vel -= 1

        abs_vol = 10*abs(5-self.abs_vel)
        #Changes ball color based on speed
        if self.BALL_COLOR[1] - abs_vol*2 > 0:
            self.BALL_COLOR = (self.BALL_COLOR[0], self.BALL_COLOR[1]-2*abs_vol, self.BALL_COLOR[2]-2*abs_vol)

    def round_over(self, side_to_point):
        """
        Resets position of ball and blocks and calls countdown timer
        """
        self.ball_x = self.size[0] / 2
        self.ball_y = self.size[1] / 2
        
        #Resets x velocity to go in direction of winner on first attempt
        numbers_x = range(1,4)
        self.ball_xv = random.choice(numbers_x)
        if side_to_point == 0:
            self.ball_xv *= -1

        #Resets y velocity at random from range [-2,0) U (0, 2]
        numbers_y = range(-2,0) + range(1,3)
        self.ball_yv = random.choice(numbers_y)

        self.side_score[side_to_point] += 1
        self.pos_dict[0] = self.size[1] / 2
        self.pos_dict[1] = self.size[1] / 2
        self.BALL_COLOR = (255,255,255)
        self.screen.fill(self.BLACK)
        self.drawBlocks()
        self.drawBall()
        pygame.display.flip()
        for i in range(3,0, -1):
            self.countDown(str(i))
            pygame.time.wait(500)
                    
    
    def countDown(self, i):
        self.countdown = self.font.render(i,True, self.BLACK, self.WHITE) 
        textRect = self.countdown.get_rect()  
        textRect.center = (self.size[0]/2, self.size[1]/2)
        self.screen.blit(self.countdown,textRect)
        pygame.display.flip()


py_game = game_env()
