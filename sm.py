import pygame, sys
from pygame.locals import *
import random
from discoIPC import ipc
import time

client_id = "530330721911439381"
client = ipc.DiscordIPC(client_id)
client.connect()

baseActivity = {
    'details': 'In the main menu',
    'timestamps': {},
    'assets': {
        'small_image': 'PyManiaLogo',
        'small_text': 'PyMania',
    }
}

menuActivity = {
    'details': 'In the main menu',
    'timestamps': {},
    'assets': {
        'small_image': 'PyManiaLogo',
        'small_text': 'PyMania',
    }
}

pygame.init()
windowIcon = pygame.image.load("assets/PyManiaLogo.png")
pygame.display.set_icon(windowIcon)
windowSurface = pygame.display.set_mode((1280, 720), 0, 32)
windowTagLines = ["StepMania, but in python", "SnakeMania", "My keyboard broke",
                  "This probably won't work", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"]
pygame.display.set_caption('PyMania: ' + windowTagLines[random.randint(0, 4)])

fallbackFont = pygame.font.SysFont(None, 48)

def set_activity(songName):
    activity = baseActivity
    activity['state'] = 'Playing Level {0}'.format(songName)
    activity['timestamps']['start'] = time.time()
    activity['assets']['large_image'] = 'level_{0}'.format(songName)
    activity['assets']['large_text'] = 'Level {0}'.format(songName)
    return activity

def mainMenu():
    client.update_activity(menuActivity)
    pygame.mixer.music.load("assets/menu.ogg")
    pygame.mixer.music.play(-1)
    menuTextColor = (0, 0, 0)
    menuBackgroundColor = (255, 255, 255)
    menuFont = pygame.font.Font("assets/mainMenu.ttf", 92)
    gameTitleText = menuFont.render('PyMania', True, menuTextColor)
    textRect = gameTitleText.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery - 280
    windowSurface.fill(menuBackgroundColor)
    pixArray = pygame.PixelArray(windowSurface)
    pixArray[480][380] = menuTextColor
    del pixArray
    windowSurface.blit(gameTitleText, textRect)
    pygame.display.update()


def testLoop():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

mainMenu()
testLoop()
