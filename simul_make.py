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

# Rect objects for each of the four buttons
YELLOWRECT = pygame.Rect(XMARGIN,YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAP, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAP, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAP, YMARGIN + BUTTONSIZE + BUTTONGAP, BUTTONSIZE, BUTTONSIZE )

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.Font('freesansbold.ttf',16)
    
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHIGHT -25)
    # load the sound files
    BEEP1 = pygame.mixer.Sound('beep1.org')
    BEEP2 = pygame.mixer.Sound('beep2.org')
    BEEP3 = pygame.mixer.Sound('beep3.org')
    BEEP4 = pygame.mixer.Sound('beep4.org')

    # Initialize some variables for a new game
    pattern = []
    currentStep = 0
    lastClickTime = 0
    score = 0
    # when False, the pattern is playing. when True, waiting for the player to click a colored button:
    waitingForInput = False

    while True:
        clickedButton = None
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topLeft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDONW:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s: 
                    clicked = GREEN



        if not waitingForInput:
            # play the pattern
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice(YELLOW, BLUE, RED, GREEN))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            #
            if clickedButton and clickedButton == pattern[currentStep]:
                #
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    #
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0

                elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime ):
                    #
                    gameOverAnimation()
                    #
                    pattern = []
                    currentStep = 0 
                    waitingForInput = False
                    score = 0 
                    pygame.time.wait(1000)
                    changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)
    

def flashButtonAnimation(color, animationSpeed =  50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0,255,1), (255,0, -1)):
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf,(0,0))
            flashSurf.fill((r,g,b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
        DISPLAYSURF.blit(origSurf, (0,0))


def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)


def changeBackgroundAnimation(animationSpeed = 40):
    global bgColor
    newBgColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r,g,b = newBgColor
    for alpha in range(0,255,animationSpeed):
        checkForQuit()
        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill(r,g,b,alpha)
        DISPLAYSURF.blit(newBgSurf, (0,0))

        drawButtons()

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor
    

def gameOverAnimation(color= WHITE, animationSpeed = 50):

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r,g,b = color
    for i in range(3):
        for start, end, step in ((0,255,1),(255,0,-1)):


            for alpha in range(start, end, animationSpeed * step):

                checkForQuit()
                flashSurf.fill(r,g,b,alpha)
                DISPLAYSURF.blit(origSurf, (0,0))
                DISPLAYSURF.blit(flashSurf, (0,0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)



def getButtonClicked(x,y):
    if YELLOWRECT.collidepiont((x,y)):
        return YELLOW
    elif BLUERECT.collidepiont((x,y)):
        return BLUE
    elif REDRECT.collidepiont((x,y)):
        return RED
    elif GREENRECT.collidepiont((x,y)):
        return GREEN
    return None


if __name__=='__name__':
    main()
