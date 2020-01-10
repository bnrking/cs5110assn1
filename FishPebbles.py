# Fish Pebbles (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys, math
from pygame.locals import *

FPS = 5
WINDOWWIDTH = 740
WINDOWHEIGHT = 580
CELLSIZE = 20
RADIUS = math.floor(CELLSIZE / 2.5)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
BLUE = (173, 216, 230)
PURPLE = (106, 13, 173)
PINK = (255, 20, 147)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # syntactic sugar: index of the worm's head
HEAD2 = 0


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('FishPebbles')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx1 = random.randint(5, CELLWIDTH - 6)
    starty1 = random.randint(5, CELLHEIGHT - 6)

    startx2 = random.randint(5, CELLWIDTH - 6)
    starty2 = random.randint(5, CELLHEIGHT - 6)

    wormCoords = [{'x': startx1, 'y': starty1},
                  {'x': startx1 - 1, 'y': starty1},
                  {'x': startx1 - 2, 'y': starty1}]
    worm2Coords = [{'x1': startx2, 'y1': starty2},
                   {'x1': startx2 - 1, 'y1': starty2},
                   {'x1': startx2 - 2, 'y1': starty2}]
    direction = RIGHT
    direction2 = RIGHT

    # Start the apple in a random place.

    apple = getRandomLocation()
    apple2 = getRandomLocation()
    core = getRandomLocation()




    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_KP4) and direction != RIGHT and direction2 != RIGHT:
                    direction = LEFT
                    direction2 = LEFT
                elif (event.key == K_KP6) and direction != LEFT and direction2 != LEFT:
                    direction = RIGHT
                    direction2 = RIGHT
                elif (event.key == K_KP8) and direction != DOWN and direction2 != DOWN:
                    direction = UP
                    direction2 = UP
                elif (event.key == K_KP2) and direction != UP and direction2 != UP:
                    direction = DOWN
                    direction2 = DOWN
                elif (event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_s) and direction != UP:
                    direction = DOWN
                elif(event.key == K_LEFT) and direction2 != RIGHT:
                    direction2 = LEFT
                elif (event.key == K_RIGHT) and direction2 != LEFT:
                    direction2 = RIGHT
                elif (event.key == K_UP) and direction2 != DOWN:
                    direction2 = UP
                elif (event.key == K_DOWN) and direction2 != UP:
                    direction2 = DOWN
                elif event.key == K_ESCAPE:
                    terminate()


        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or \
                wormCoords[HEAD]['y'] == CELLHEIGHT or worm2Coords[HEAD2]['x1'] == -1 or worm2Coords[HEAD2]['x1'] == \
                CELLWIDTH or worm2Coords[HEAD2]['y1'] == -1 or worm2Coords[HEAD2]['y1'] == CELLHEIGHT:
            return  # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # game over
        for worm2Body in worm2Coords[1:]:
            if worm2Body['x1'] == worm2Coords[HEAD2]['x1'] and worm2Body['y1'] == worm2Coords[HEAD2]['y1']:
                return  # gameover

         ##TODO: ADD RUNING INTO CORE = GAMEOVER
        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation()# set a new apple somewhere
            drawAppleCore(core)#droping apple cores


        elif wormCoords[HEAD]['x'] == apple2['x'] and wormCoords[HEAD]['y'] == apple2['y']:
            apple2 = getRandomLocation()
            drawAppleCore(core)
            # drawAppleCore(tea) #droping apple cores

        else:
            del wormCoords[-1]  # remove worm's tail segment

        if worm2Coords[HEAD]['x1'] == apple['x'] and worm2Coords[HEAD]['y1'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation()  # set a new apple somewhere
            drawAppleCore(core)
             #droping apple cores
        elif worm2Coords[HEAD]['x1'] == apple2['x'] and worm2Coords[HEAD]['y1'] == apple2['y']:
            apple2 = getRandomLocation()
            drawAppleCore(core) #droping apple cores

        else:
            del worm2Coords[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
            # newHead2 = {'x1': worm2Coords[HEAD2]['x1'], 'y1': worm2Coords[HEAD2]['y1'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
            # newHead2 = {'x1': worm2Coords[HEAD2]['x1'], 'y1': worm2Coords[HEAD2]['y1'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
            # newHead2 = {'x1': worm2Coords[HEAD2]['x1'] - 1, 'y1': worm2Coords[HEAD2]['y1']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
            # newHead2 = {'x1': worm2Coords[HEAD2]['x1'] + 1, 'y1': worm2Coords[HEAD2]['y1']}
        wormCoords.insert(0, newHead)  # have already removed the last segment
        # move the worm by adding a segment in the direction it is moving

        if direction2 == UP:
            newHead2 = {'x1': worm2Coords[HEAD2]['x1'], 'y1': worm2Coords[HEAD2]['y1'] - 1}
        elif direction2 == DOWN:
            newHead2 = {'x1': worm2Coords[HEAD2]['x1'], 'y1': worm2Coords[HEAD2]['y1'] + 1}
        elif direction2 == LEFT:
            newHead2 = {'x1': worm2Coords[HEAD2]['x1'] - 1, 'y1': worm2Coords[HEAD2]['y1']}
        elif direction2 == RIGHT:
            newHead2 = {'x1': worm2Coords[HEAD2]['x1'] + 1, 'y1': worm2Coords[HEAD2]['y1']}
        worm2Coords.insert(0, newHead2)

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawWorm2(worm2Coords)
        drawApple(apple)
        drawApple(apple2)

        drawScore(len(wormCoords) - 3)
        drawScore2(len(worm2Coords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, MAGENTA)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('USU', True, WHITE, BLUE)
    titleSurf2 = titleFont.render('Agents', True, PURPLE)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (math.floor(WINDOWWIDTH / 2), 10)
    overRect.midtop = (math.floor(WINDOWWIDTH / 2), gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawScore(score):
    scoreSurf = BASICFONT.render('Pink Worm Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 180, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawScore2(score2):
    scoreSurf2 = BASICFONT.render('Blue Worm Score: %s' % (score2), True, WHITE)
    scoreRect2 = scoreSurf2.get_rect()
    scoreRect2.topleft = (WINDOWWIDTH - 180, 30)
    DISPLAYSURF.blit(scoreSurf2, scoreRect2)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, MAGENTA, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, PINK, wormInnerSegmentRect)


def drawWorm2(worm2Coords):
    for coord in worm2Coords:
        x1 = coord['x1'] * CELLSIZE
        y1 = coord['y1'] * CELLSIZE
        wormSegmentRect1 = pygame.Rect(x1, y1, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, BLUE, wormSegmentRect1)
        wormInnerSegmentRect1 = pygame.Rect(x1 + 4, y1 + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, BLACK, wormInnerSegmentRect1)


def drawApple(coord):
    # ADD MORE APPLE
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    xcenter = coord['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
    ycenter = coord['y'] * CELLSIZE + math.floor(CELLSIZE / 2)
    x1center = coord['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
    y1center = coord['y'] * CELLSIZE + math.floor(CELLSIZE / 2)
    # appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    # pygame.draw.rect(DISPLAYSURF, RED, appleRect)
    pygame.draw.circle(DISPLAYSURF, RED, (xcenter, ycenter), RADIUS)
    pygame.draw.circle(DISPLAYSURF, RED, (x1center, y1center), RADIUS)


def drawAppleCore(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    xcoreCenter = coord['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
    ycorecenter = coord['y'] * CELLSIZE + math.floor(CELLSIZE / 2)
    x1corecenter = coord['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
    y1corecenter = coord['y'] * CELLSIZE + math.floor(CELLSIZE / 2)
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
