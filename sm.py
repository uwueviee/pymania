import pygame, sys
from pygame.locals import *
import random

pygame.init()

windowSurface = pygame.display.set_mode((500, 400), 0, 32)
windowTagLines = ["StepMania, but in python", "SnakeMania", "My keyboard broke",
                  "This probably won't work", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"]
pygame.display.set_caption('PyMania: ' + windowTagLines[random.randint(0, 4)])

fallbackFont = pygame.font.SysFont(None, 48)

def mainMenu():
    menuTextColor = (0, 0, 0)
    menuBackgroundColor = (255, 255, 255)
    menuFont = pygame.font.SysFont(None, 48)
    text = menuFont.render('owo', True, menuTextColor)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery - 50
    windowSurface.fill(menuBackgroundColor)
    pixArray = pygame.PixelArray(windowSurface)
    pixArray[480][380] = menuTextColor
    del pixArray
    windowSurface.blit(text, textRect)
    pygame.display.update()

def testLoop():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

mainMenu()
testLoop()