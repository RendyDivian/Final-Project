import pygame, sys, random, time, math
from pygame.locals import*

pygame.init()

#Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

screenx = 1000
screeny = 600

windowSurface = pygame.display.set_mode((screenx, screeny), 0, 0)

#The pictures used (person and green squares)
person1 = pygame.image.load("mc.bmp")
personpic = pygame.transform.scale(person1, (40, 50))
personpic.convert()

startpoint = pygame.image.load("starting.bmp")
greenImage1 = pygame.transform.scale(startpoint, (100, 100))
greenImage1.convert()

endpoint = pygame.image.load("ending.bmp")
greenImage2 = pygame.transform.scale(endpoint, (70, 70))
greenImage2.convert()

# Sets the position of the green squares
# Position in x and y coordinates (x=left, right and y=up, down)
# Starting square
greenRectA = greenImage1.get_rect()
greenRectA.centerx = 50
greenRectA.centery = 550

# Finishing square
greenRectB = greenImage2.get_rect()
greenRectB.centerx = 950
greenRectB.centery = 50

fireballpic = pygame.image.load("fireballicon.bmp")
fireball = pygame.transform.scale(fireballpic, (60, 60))
fireball.set_colorkey(WHITE) #To make the fireball background transparent
fireball.convert()

class Aperson():
    def __init__(self, Image):
        self.speed = 5
        self.directionx = 0
        self.directiony = 0
        self.image = Image
        self.rect = self.image.get_rect()

    def move(self):
        self.rect.centerx = self.rect.centerx + self.speed * self.directionx
        self.rect.centery = self.rect.centery + self.speed * self.directiony


hero = Aperson(personpic)
#Sets the position of the player
hero.rect.centerx = greenRectA.centerx
hero.rect.centery = greenRectA.centery
#Sets the speed of the player
hero.speed = 7

#Sets number of enemies
numberfireball = 3
enemy = [Aperson(fireball) for i in range(0, numberfireball)]
#Centerx and centery is the position
#Directionx and directiony show which way the enemy is moving
#Directionx=1 is right, -1 is left, directiony=1 is down, -1 is up
#One enemy
enemy[0].rect.centerx = 500
enemy[0].rect.centery = 0
enemy[0].directionx = 0
enemy[0].directiony = -1
enemy[0].speed = 10
#Second enemy
enemy[1].rect.centerx = 0
enemy[1].rect.centery = 350
enemy[1].directionx = 1
enemy[1].directiony = 0
enemy[1].speed = 6
#Third Enemy
enemy[2].rect.centerx = 300
enemy[2].rect.centery = 250
enemy[2].directionx = 0
enemy[2].directiony = 1
enemy[2].speed = 6
# Change number up above and add another enemy section to create more enemies


pygame.display.set_caption('Dodge Game')

moveRight = False
moveLeft = False
moveUp = False
moveDown = False

gameOver = False

pygame.display.update()

while gameOver == False:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # Checks when the arrow keys or escape are pressed
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            gameOver = True
        if event.key == K_LEFT:
            moveLeft = True
        if event.key == K_RIGHT:
            moveRight = True
        if event.key == K_UP:
            moveUp = True
        if event.key == K_DOWN:
            moveDown = True
    # Checks when they are released
    if event.type == KEYUP:
        if event.key == K_LEFT:
            moveLeft = False
        if event.key == K_RIGHT:
            moveRight = False
        if event.key == K_UP:
            moveUp = False
        if event.key == K_DOWN:
            moveDown = False
    # Moves the character
    if moveRight == True:
        hero.rect.centerx = hero.rect.centerx + hero.speed
    if moveLeft == True:
        hero.rect.centerx = hero.rect.centerx - hero.speed
    if moveUp == True:
        hero.rect.centery = hero.rect.centery - hero.speed
    if moveDown == True:
        hero.rect.centery = hero.rect.centery + hero.speed

    #Blocks the player from going off the screen
    if hero.rect.centerx < 0:
        hero.rect.centerx = 0
    if hero.rect.centerx > screenx:
        hero.rect.centerx = screenx
    if hero.rect.centery < 0:
        hero.rect.centery = 0
    if hero.rect.centery > screeny:
        hero.rect.centery = screeny

    windowSurface.fill(GRAY)
    #Blocks the enemy
    windowSurface.blit(greenImage1, greenRectA)
    windowSurface.blit(greenImage2, greenRectB)
    windowSurface.blit(hero.image, hero.rect)
    for i in range(0, numberfireball):
        windowSurface.blit(enemy[i].image, enemy[i].rect)
        enemy[i].move()
        if enemy[i].rect.centery < 0:
            enemy[i].directiony = 1
        if enemy[i].rect.centery > screeny:
            enemy[i].directiony = -1
        if enemy[i].rect.centerx < 0:
            enemy[i].directionx = 1
        if enemy[i].rect.centerx > screenx:
            enemy[i].directionx = -1

        #Checks when you collide with an enemy and says that you lost
        if enemy[i].rect.colliderect(hero.rect):
            bigFont = pygame.font.SysFont('arial', 60)
            myMessage = bigFont.render('You lost!', True, RED, BLACK)
            myMessageRect = myMessage.get_rect()
            myMessageRect.centerx = screenx / 2
            myMessageRect.centery = screeny / 2
            windowSurface.blit(myMessage, myMessageRect)
            pygame.display.update()
            time.sleep(1.5)
            gameOver = True

    #Checks when you collide with the ending square and says that you won
    if hero.rect.colliderect(greenRectB):
        bigFont = pygame.font.SysFont('arial', 60)
        myMessage = bigFont.render('You won!', True, YELLOW, BLACK)
        myMessage.set_colorkey(BLACK)
        myMessageRect = myMessage.get_rect()
        myMessageRect.centerx = screenx / 2
        myMessageRect.centery = screeny / 2
        windowSurface.blit(myMessage, myMessageRect)
        pygame.display.update()
        time.sleep(1.5)
        gameOver = True

    pygame.display.update()
    time.sleep(0.02)

pygame.quit()