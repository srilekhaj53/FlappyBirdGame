import random
import sys #we will use sys.exit to exit the program
import pygame
from pygame.locals import * #Basic pygame imports
#Global variables
FPS=32 #frames per second
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='C:/Pythonprojects/pythonProject1/gallery_p/sprites/bird.png'
BACKGROUND='C:/Pythonprojects/pythonProject1/gallery_p/sprites/background.png'
PIPE = 'C:/Pythonprojects/pythonProject1/gallery_p/sprites/pipe.png'
def welcomeScreen():
    print("Welcome screen is loading...") 
    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex=int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey=int(SCREENWIDTH*0.13)
    basex=0
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                print("Space or Up key pressed!")
                return 
            #SCREEN.fill((0, 0, 0))
            SCREEN.blit(GAME_SPRITES['background'],(0,0))
                # Resize images (optional)
            SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
            SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
            SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))
            pygame.display.update()
            FPSCLOCK.tick(FPS)
                                                                                                                                                                                                                                                                                                               
def mainGame():
    print("Calling getRandomPipe...")

    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0

    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()
    upperPipes=[
        {'x':SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']}
    ]
    lowerPipes=[
        {'x':SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']}
    ]
    pipeVelX = -4

    playerVelY=-9
    playerMaxVelY=10
    playerMinVelY=-8
    playerAccY=1

    playerFlapAccv=-8 #velocity while flapping
    playerFlapped=False

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
                print("HI")
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery > 0:
                    playerVelY+=playerFlapAccv
                    playerFlapped=True
                    GAME_SOUNDS['wing'].play()
        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return
        #chech for score
        playerMidpos=playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos=pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<=playerMidpos<pipeMidPos+4:
                score+=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play() 
        if playerVelY<playerMaxVelY and not playerFlapped:
            playerVelY=playerAccY
        if playerFlapped:
            playerFlapped=False
        playerHeight=GAME_SPRITES['player'].get_height()
        playery=playery+min(playerVelY,GROUNDY-playery-playerHeight)
        #move pipes to left
        for upperPipe,lowerpipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipeVelX
            lowerpipe['x']+=pipeVelX
        #add a new pipe when pipe is about to cross  leftmost part of screen
        if 0<upperPipes[0]['x']<5:
            newpipe=getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        #if pipe is out of screen, remove it
        if upperPipes[0]['x']<= -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
        myDigits= [int(x) for x in list(str(score))]
        width=0
        for digit in myDigits:
            width+=GAME_SPRITES['numbers'][digit].get_width()
        Xoffset=(SCREENWIDTH-width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset+=GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def isCollide(playerx,playery,upperPipes, lowerPipes):
    if playery> GROUNDY-25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight= GAME_SPRITES['pipe'][0].get_height()
        if( playery < pipeHeight+ pipe['y'] and abs(playerx -pipe['x']) <GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes: 
        if( playery+GAME_SPRITES['player'].get_height()> pipe['y'] ) and abs(playerx -pipe['x']) <GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False
def getRandomPipe():
    
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3
    max_y = int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.5 * offset)
    if max_y<=0:
        max_y=50
    print("Base height:", GAME_SPRITES['base'].get_height())
    print("Pipe height:", pipeHeight)
    print("Offset:", offset)
    print("max_y:", max_y)
    y2=offset+random.randrange(0,max_y)
    pipeX=SCREENWIDTH+10
    y1=pipeHeight-y2+offset
    pipe=[
        {'x':pipeX, 'y':-y1},
        {'x':pipeX, 'y':y2}
    ]
    return pipe
if __name__=="__main__":
    #game starts
    pygame.init() #initialize pygame modules
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Srilekha')
    number_images = []
    for i in range(10):
        num_img = pygame.image.load(f'C:/Pythonprojects/pythonProject1/gallery_p/sprites/{i}.png').convert_alpha()
        scaled_img = pygame.transform.scale(num_img, (25, 35))
        number_images.append(scaled_img)
    GAME_SPRITES['numbers'] = tuple(number_images)
    #GAME_SPRITES['message']=pygame.image.load('C:\\Pythonprojects\\pythonProject1\\gallery_p\\sprites\\message.jpg').convert_alpha()
    original_msg = pygame.image.load('C:/Pythonprojects/pythonProject1/gallery_p/sprites/message.jpg').convert_alpha()
    GAME_SPRITES['message'] = pygame.transform.scale(original_msg, (200, 100))  # scale to a smaller size like 200x100

    GAME_SPRITES['base']=pygame.image.load('C:\\Pythonprojects\\pythonProject1\\\gallery_p\\sprites\\base.png').convert_alpha()
    pipe_image = pygame.image.load(PIPE).convert_alpha()
    pipe_image = pygame.transform.scale(pipe_image, (80, 500))
    GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pipe_image, 180),  # upper pipe
    pipe_image  # lower pipe
)
    #AME_SPRITES['pipe']=(
      # pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
       #pygame.image.load(PIPE).convert_alpha()
    #
    #Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('C:/Pythonprojects/pythonProject1/gallery_p/audio/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('C:/Pythonprojects/pythonProject1/gallery_p/audio/hit.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('C:/Pythonprojects/pythonProject1/gallery_p/audio/point.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('C:/Pythonprojects/pythonProject1/gallery_p/audio/swoosh.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('C:/Pythonprojects/pythonProject1/gallery_p/audio/wing.mp3')


    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert()
    original_player = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['player'] = pygame.transform.scale(original_player, (50, 50))  # scale to a smaller size like 50x50

    print("Player size:", GAME_SPRITES['player'].get_size())
    print("Message size:", GAME_SPRITES['message'].get_size())

    while(True):
        welcomeScreen()
        print("Base height:", GAME_SPRITES['base'].get_height())
        mainGame()
