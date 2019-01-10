import pygame
import sys
from pygame.locals import *
import random
from discoIPC import ipc
import time
import re
import json
#import ChromaPython

#Info = ChromaPython.ChromaAppInfo()
#Info.DeveloperName = 'Skye Viau'
#Info.DeveloperContact = 'skye.viau@gmail.com'
#Info.Category = 'application'
#Info.SupportedDevices = ['keyboard', 'mouse', 'mousepad']
#Info.Description = 'Step Mania clone made in Python and Pygame'
#Info.Title = 'PyMania'

#App = ChromaPython.ChromaApp(Info)
#KeyboardGrid = ChromaPython.ChromaGrid('Keyboard')
#MouseGrid = ChromaPython.ChromaGrid('Mouse')
#MousepadGrid = ChromaPython.ChromaGrid('Mousepad')

#KeyboardGrid.set(hexcolor="#FF0000")
#MousepadGrid.set(red=255, blue=0, green=0)
#MouseGrid.set(hexcolor="0xFF0000")


# TODO: Find a replacement for discoIPC since it's broken on Windows
client_id = "530330721911439381"
client = ipc.DiscordIPC(client_id)
#client.connect()

baseActivity = {
    'details': 'In the main menu',
    'timestamps': {},
    'assets': {
        'large_image': 'pymanialogo',
        'large_text': 'PyMania',
    }
}

menuActivity = {
    'state': 'testing',
    'details': 'In the main menu',
    'timestamps': {},
    'assets': {
        'large_image': 'pymanialogo',
        'large_text': 'PyMania',
    }
}

pygame.init()
clock = pygame.time.Clock()
clock.tick(60)
windowIcon = pygame.image.load("assets/PyManiaLogo.png")
gameTitle = pygame.image.load("assets/PyManiaLogoText.png")
pygame.display.set_icon(windowIcon)
windowSurface = pygame.display.set_mode((1280, 720), 0, 32)
windowTagLines = ["StepMania, but in python", "SnakeMania", "My keyboard broke",
                  "This probably won't work", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                  "Blame windows for Discord RPC not working"]
pygame.display.set_caption('PyMania: ' + windowTagLines[random.randint(0, 4)])

with open("songs/songList.json") as f:
    songDatabase = json.load(f)

fallbackFont = pygame.font.SysFont(None, 48)

mainMenuMusic = 0


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def set_activity(songName):
    activity = baseActivity
    activity['state'] = 'Playing Level {0}'.format(songName)
    activity['timestamps']['start'] = time.time()
    activity['assets']['large_image'] = 'level_{0}'.format(songName)
    activity['assets']['large_text'] = 'Level {0}'.format(songName)
    return activity


def mainMenu():
    global mainMenuMusic
    # Discord RPC
    #client.update_activity(menuActivity)
    # Load sound files and play menu music
    if mainMenuMusic == 0:
        pygame.mixer.music.load("assets/menu.ogg")
        pygame.mixer.music.play(-1)
        mainMenuMusic = 1
    clickSound = pygame.mixer.Sound("assets/click.ogg")

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
                selectMode()

        if quitRect.x+quit.get_width() > mouse[0] > quitRect.x and quitRect.y+quit.get_height() > mouse[1] > quitRect.y:
            if click[0] == 1:
                clickSound.set_volume(0.6)
                clickSound.play()
                pygame.quit()
                sys.exit()


def selectMode():
    clickSound = pygame.mixer.Sound("assets/click.ogg")

    # Define main menu only colors
    menuBackgroundColor = (52, 52, 52)
    menuTextColor = (240, 240, 240)

    # Buttons
    buttonFont = pygame.font.Font('assets/mainMenu.ttf', 45)
    modeTitleFont = pygame.font.Font('assets/mainMenu.ttf', 100)

    gameTitleMenu = modeTitleFont.render('SELECT A MODE', True, menuTextColor)
    titleRect = gameTitleMenu.get_rect()
    titleRect.centerx = windowSurface.get_rect().centerx
    titleRect.centery = windowSurface.get_rect().centery - 150

    start = buttonFont.render('SOLO', True, menuTextColor)
    startRect = start.get_rect()
    startRect.centerx = windowSurface.get_rect().centerx - 120
    startRect.centery = windowSurface.get_rect().centery + 50

    quit = buttonFont.render('VERSUS', True, menuTextColor)
    quitRect = quit.get_rect()
    quitRect.centerx = windowSurface.get_rect().centerx + 120
    quitRect.centery = windowSurface.get_rect().centery + 50

    nonstop = buttonFont.render('NONSTOP', True, menuTextColor)
    nonstopRect = nonstop.get_rect()
    nonstopRect.centerx = windowSurface.get_rect().centerx
    nonstopRect.centery = windowSurface.get_rect().centery + 150

    back = buttonFont.render('BACK', True, menuTextColor)
    backRect = back.get_rect()
    backRect.centerx = windowSurface.get_rect().centerx - 550
    backRect.centery = windowSurface.get_rect().centery + 330

    # Draw everything to window
    windowSurface.fill(menuBackgroundColor)
    windowSurface.blit(gameTitleMenu, titleRect)
    windowSurface.blit(start, startRect)
    windowSurface.blit(quit, quitRect)
    windowSurface.blit(nonstop, nonstopRect)
    windowSurface.blit(back, backRect)

    # Make the menu I N T E R A C T I V E
    time.sleep(0.1)
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
                pickSong()

        if quitRect.x+quit.get_width() > mouse[0] > quitRect.x and quitRect.y+quit.get_height() > mouse[1] > quitRect.y:
            if click[0] == 1:
                clickSound.set_volume(0.6)
                clickSound.play()
                testLoop()

        if nonstopRect.x+nonstop.get_width() > mouse[0] > nonstopRect.x and nonstopRect.y+nonstop.get_height() > mouse[1] > nonstopRect.y:
            if click[0] == 1:
                clickSound.set_volume(0.6)
                clickSound.play()
                testLoop()

        if backRect.x+back.get_width() > mouse[0] > backRect.x and backRect.y+back.get_height() > mouse[1] > backRect.y:
            if click[0] == 1:
                clickSound.set_volume(0.6)
                clickSound.play()
                mainMenu()


def pickSong():
    clickSound = pygame.mixer.Sound("assets/click.ogg")
    startSound = pygame.mixer.Sound("assets/startSong.ogg")

    # Define main menu only colors
    menuBackgroundColor = (52, 52, 52)
    menuTextColor = (240, 240, 240)

    # Draw everything to window
    windowSurface.fill(menuBackgroundColor)

    buttonFont = pygame.font.Font('assets/mainMenu.ttf', 45)
    modeTitleFont = pygame.font.Font('assets/mainMenu.ttf', 55)

    gameTitleMenu = modeTitleFont.render('SELECT A SONG', True, menuTextColor)
    titleRect = gameTitleMenu.get_rect()
    titleRect.centerx = windowSurface.get_rect().centerx - 390
    titleRect.centery = windowSurface.get_rect().centery - 310

    back = buttonFont.render('BACK', True, menuTextColor)
    backRect = back.get_rect()
    backRect.centerx = windowSurface.get_rect().centerx - 550
    backRect.centery = windowSurface.get_rect().centery + 330

    test = buttonFont.render('TEST', True, menuTextColor)
    testRect = test.get_rect()
    testRect.centerx = windowSurface.get_rect().centerx
    testRect.centery = windowSurface.get_rect().centery

    windowSurface.blit(back, backRect)
    windowSurface.blit(gameTitleMenu, titleRect)
    windowSurface.blit(test,testRect)

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
        if backRect.x+back.get_width() > mouse[0] > backRect.x and backRect.y+back.get_height() > mouse[1] > backRect.y:
            if click[0] == 1:
                clickSound.set_volume(0.6)
                clickSound.play()
                selectMode()
        if testRect.x+test.get_width() > mouse[0] > testRect.x and testRect.y+test.get_height() > mouse[1] > testRect.y:
            if click[0] == 1:
                startSound.set_volume(0.6)
                startSound.play()
                playSong("cardofyourdreams", 1)


def playSong(songName, difficulty):
    print(songName, difficulty)

    # Declare colors
    textColor = (240, 240, 240)
    menuBackgroundColor = (52, 52, 52)

    # Look for song location in song database
    songLocation = songDatabase[songName]["folder"]

    # Load data
    smFile = open("songs/" + songLocation + "/" + songDatabase[songName]["sm"], "r")
    smData = []
    for line in smFile:
        for words in line.strip().split(';'):
            smData.append(words)
    smData = filter(None, smData)
    print smData
    try:
        songProperName = re.sub('^[^:]+[:]', '', smData[0])
        songArtist = re.sub('^[^:]+[:]', '', smData[2])
        songBPM = re.sub('^[^:]+[:]', '', smData[17])
        songBPM = re.sub('^[^=]*=', '', songBPM)
        songBackground = re.sub('^[^:]+[:]', '', smData[9])
        songTrack = re.sub('^[^:]+[:]', '', smData[12])
    except:
        pass
    try:
        songProperName = re.sub('^[^:]+[:]', '', smData[0])
        songArtist = re.sub('^[^:]+[:]', '', smData[2])
        songBPM = re.sub('^[^:]+[:]', '', smData[16])
        songBPM = re.sub('^[^=]*=', '', songBPM)
        songBackground = re.sub('^[^:]+[:]', '', smData[8])
        songTrack = re.sub('^[^:]+[:]', '', smData[11])
    except:
        pass
    print songProperName
    print songArtist
    print songBPM
    print songBackground
    print songTrack

    # Set background
    windowSurface.fill(menuBackgroundColor)
    BackGround = Background('songs/'+songLocation+'/'+songBackground, [0, 0])

    # Load song
    pygame.mixer.music.load("songs/" + songLocation + "/" + songTrack)

    # Declare fonts
    miscFont = pygame.font.Font('assets/mainMenu.ttf', 45)
    songTitleFont = pygame.font.Font('assets/mainMenu.ttf', 55)

    songTitle = songTitleFont.render(songName, True, textColor)
    titleRect = songTitle.get_rect()
    titleRect.centerx = windowSurface.get_rect().centerx - 390
    titleRect.centery = windowSurface.get_rect().centery - 310

    back = miscFont.render('BACK', True, textColor)
    backRect = back.get_rect()
    backRect.centerx = windowSurface.get_rect().centerx - 550
    backRect.centery = windowSurface.get_rect().centery + 330

    countDown = miscFont.render('NA', True, textColor)
    countRect = countDown.get_rect()
    countRect.centerx = windowSurface.get_rect().centerx
    countRect.centery = windowSurface.get_rect().centery

    windowSurface.blit(BackGround.image, BackGround.rect)
    firstLaunch = 1
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if firstLaunch == 1:
            countDown = miscFont.render('3', True, textColor)
            windowSurface.blit(countDown, countRect)
            pygame.display.update()
            time.sleep(1)
            countDown = miscFont.render('2', True, textColor)
            windowSurface.blit(countDown, countRect)
            pygame.display.update()
            time.sleep(1)
            countDown = miscFont.render('1', True, textColor)
            windowSurface.blit(countDown, countRect)
            pygame.display.update()
            time.sleep(1)
            pygame.mixer.music.play()
            firstLaunch = 0
        else:
            if pygame.mixer.music.get_busy() == False:
                scoreScreen(songName, score, difficulty)
                pygame.display.update()


def scoreScreen(songName, score, difficulty):
    print(songName, score, difficulty)

    global mainMenuMusic

    # Load sound files and play menu music
    if mainMenuMusic == 0:
        pygame.mixer.music.load("assets/menu.ogg")
        pygame.mixer.music.play(-1)
        mainMenuMusic = 1

    # Declare colors
    textColor = (240, 240, 240)
    menuBackgroundColor = (52, 52, 52)

    # Set background
    windowSurface.fill(menuBackgroundColor)

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


def debugArea():
    print("WARNING: THIS AREA CAN DAMAGE USER PROFILES")

def testLoop():
    clickSound = pygame.mixer.Sound("assets/click.ogg")
    # Define meme
    rect1_x = random.randint(1, 1159)
    rect1_y = random.randint(1, 589)
    rect2_x = random.randint(1, 1159)
    rect2_y = random.randint(1, 589)
    rect3_x = random.randint(1, 1159)
    rect3_y = random.randint(1, 589)
    rect1xSpeed = random.randint(3, 6)
    rect1ySpeed = random.randint(3, 6)
    rect2xSpeed = random.randint(7, 9)
    rect2ySpeed = random.randint(7, 9)
    rect3xSpeed = random.randint(10, 12)
    rect3ySpeed = random.randint(10, 12)
    gameLogoMeme = pygame.transform.smoothscale(windowIcon, (128, 128))

    # Define main menu only colors
    menuBackgroundColor = (52, 52, 52)
    menuTextColor = (240, 240, 240)

    # Draw everything to window
    windowSurface.fill(menuBackgroundColor)
    lolTextShow = 1
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        print(mouse)
        print(click)
        string1 = str(rect1_x)
        string12 = str(rect1_y)
        string2 = str(rect2_x)
        string22 = str(rect2_y)
        string3 = str(rect3_x)
        string32 = str(rect3_y)
        print "[" + string1 + "]" + "[" + string12 + "]"
        print "[" + string2 + "]" + "[" + string22 + "]"
        print "[" + string3+ "]" + "[" + string32 + "]"
        rect1_x += rect1xSpeed
        rect1_y += rect1ySpeed
        if rect1_y > 590 or rect1_y < 0:
            rect1ySpeed = rect1ySpeed * - 1
        if rect1_x > 1160 or rect1_x < 0:
            rect1xSpeed = rect1xSpeed * - 1
        rect2_x += rect2xSpeed
        rect2_y += rect2ySpeed
        if rect2_y > 590 or rect2_y < 0:
            rect2ySpeed = rect2ySpeed * - 1
        if rect2_x > 1160 or rect2_x < 0:
            rect2xSpeed = rect2xSpeed * - 1
        rect3_x += rect3xSpeed
        rect3_y += rect3ySpeed
        if rect3_y > 590 or rect3_y < 0:
            rect3ySpeed = rect3ySpeed * - 1
        if rect3_x > 1160 or rect3_x < 0:
            rect3xSpeed = rect3xSpeed * - 1
        windowSurface.fill(menuBackgroundColor)
        windowSurface.blit(gameLogoMeme, [rect1_x, rect1_y, 50, 50])
        windowSurface.blit(gameLogoMeme, [rect2_x, rect2_y, 50, 50])
        windowSurface.blit(gameLogoMeme, [rect3_x, rect3_y, 50, 50])
        buttonFont = pygame.font.Font('assets/mainMenu.ttf', 45)
        back = buttonFont.render('MENU', True, menuTextColor)
        backRect = back.get_rect()
        backRect.centerx = windowSurface.get_rect().centerx - 550
        backRect.centery = windowSurface.get_rect().centery + 330
        windowSurface.blit(back, backRect)
        if lolTextShow == 1:
            lol = buttonFont.render("IT DOESN'T EXIST", True, menuTextColor)
            lolRect = lol.get_rect()
            lolRect.centerx = windowSurface.get_rect().centerx
            lolRect.centery = windowSurface.get_rect().centery
            windowSurface.blit(lol, lolRect)
            lolTextShow = 0
        else:
            lolTextShow = 1
        pygame.display.update()
        if backRect.x+back.get_width() > mouse[0] > backRect.x and backRect.y+back.get_height() > mouse[1] > backRect.y:
            if click[0] == 1:
                clickSound.set_volume(0.6)
                clickSound.play()
                mainMenu()


mainMenu()
testLoop()
