# Simulate (a Simon clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Creative Commons BY-NC-SA 3.0 US

import random, sys, time, pygame
from pygame.locals import *

FPS = 30 
WINDOWWIDTH = 640
WINDOWHIGHT = 480
FLASHSPEED = 500
FLASHDELAY = 200
BUTTONSIZE = 200
BUTTONGAP = 20
TIMEOUT = 4

#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAP) /2)
YMARGIN = int((WINDOWHIGHT - (2 * BUTTONSIZE) - BUTTONGAP) /2)
