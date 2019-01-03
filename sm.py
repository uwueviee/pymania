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
        'large_image': 'pymanialogo',
        'large_text': 'PyMania',
    }
}

menuActivity = {
    'details': 'In the main menu',
    'timestamps': {},
    'assets': {
        'large_image': 'pymanialogo',
        'large_text': 'PyMania',
    }
}

pygame.init()
windowIcon = pygame.image.load("assets/PyManiaLogo.png")
gameTitle = pygame.image.load("assets/PyManiaLogoText.png")
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
    # Discord RPC
    client.update_activity(menuActivity)

    # Load sound files and play menu music
    pygame.mixer.music.load("assets/menu.ogg")
    clickSound = pygame.mixer.Sound("assets/click.ogg")
    pygame.mixer.music.play(-1)

    # Define main menu only colors
    menuBackgroundColor = (52, 52, 52)
    menuTextColor = (240, 240, 240)

    # PyMania game logo on menu
    gameTitleMenu = pygame.transform.smoothscale(gameTitle, (552, 276))
    titleRect = gameTitleMenu.get_rect()
    titleRect.centerx = windowSurface.get_rect().centerx
    titleRect.centery = windowSurface.get_rect().centery - 150

    # Buttons
    buttonFont = pygame.font.Font('assets/mainMenu.ttf', 45)

    start = buttonFont.render('Start Game', True, menuTextColor)
    startRect = start.get_rect()
    startRect.centerx = windowSurface.get_rect().centerx
    startRect.centery = windowSurface.get_rect().centery + 120

    quit = buttonFont.render('Quit', True, menuTextColor)
    quitRect = quit.get_rect()
    quitRect.centerx = windowSurface.get_rect().centerx
    quitRect.centery = windowSurface.get_rect().centery + 190

    # Draw everything to window
    windowSurface.fill(menuBackgroundColor)
    windowSurface.blit(gameTitleMenu, titleRect)
    windowSurface.blit(start, startRect)
    windowSurface.blit(quit, quitRect)

    # Make the menu I N T E R A C T I V E
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        print(mouse)
        print(click)
        pygame.display.update()
        if startRect.x+start.get_width() > mouse[0] > startRect.x and startRect.y+start.get_height() > mouse[1] > startRect.y:
            if click[0] == 1:
                clickSound.set_volume(0.6)
                clickSound.play()

        if quitRect.x+quit.get_width() > mouse[0] > quitRect.x and quitRect.y+quit.get_height() > mouse[1] > quitRect.y:
            if click[0] == 1:
                clickSound.set_volume(0.6)
                clickSound.play()
                pygame.quit()
                sys.exit()

def testLoop():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

mainMenu()
testLoop()
