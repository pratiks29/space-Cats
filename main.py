import pygame
import random
import math
from pygame import mixer


pygame.init()

score = 0
background = pygame.image.load('background_sB.png')

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("space cats")
icon = pygame.image.load('spacebros.png')
pygame.display.set_icon(icon)

hero = pygame.image.load('hero.png')
hero = pygame.transform.scale(hero, (64, 64))
Xcoordinate = 370
Ycoordinate = 480

font = pygame.font.Font('freesansbold.ttf',32)
over_font = pygame.font.Font('freesansbold.ttf',64)

enemy =[]
enemyX =[]
enemyY =[]
enemychangex =[]
enemychangey =[]
no_of_enemy = 5

for i in range(no_of_enemy):
    enemyb = pygame.image.load('catenemy.png')
    enemy.append(pygame.transform.scale(enemyb, (64, 64)))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 100))
    enemychangex.append( 1)
    enemychangey.append(40)

bullet = pygame.image.load('newbullet.png')
bulletX = Xcoordinate
bulletY = 480
bulletchangeX = 0
bulletchangeY = 0.8
bullet_state = "ready"
setter = Xcoordinate

textx=10
texty=10
def show_score(x,y):
    show = font.render("score: "+str(score),True,(255,255,250))
    screen.blit(show, (x, y))

def player(x, y):
    screen.blit(hero, (x, y))


def villain(x, y,i):
    screen.blit(enemy[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x, y))


def is_collision(enx, eny, bx, by):
    dist = math.sqrt(math.pow(enx-bx,2) + math.pow(eny-by,2))
    if dist <= 35:
        return True
    else:
        return False

def game_over():
    text = over_font.render(":( GAME-OVER= :(",True,(210,15,96))
    screen.blit(text,(150,250))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    xchange = 0
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            xchange = 0.3
        if event.key == pygame.K_LEFT:
            xchange = -0.3
        if event.key == pygame.K_UP and bullet_state == "ready":
            bullet_sound = mixer.Sound('bruh-sound.wav')
            bullet_sound.play()
            setter = Xcoordinate
            fire_bullet(setter, bulletY)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            xchange = 0

    Xcoordinate += xchange
    if Xcoordinate >= 736:
        Xcoordinate = 736
    elif Xcoordinate <= 0:
        Xcoordinate = 0

    screen.fill((25, 25, 25))
    screen.blit(background, (0, 0))

    for i in range(no_of_enemy):

        if enemyY[i] >420:
            for j in range(no_of_enemy):
                enemyY[j]=1000
            game_over()
            break
        enemyX[i] += enemychangex[i]
        if enemyY[i] > 540:
            enemychangey[i] = -40
        if enemyX[i] >= 736:
            enemychangex[i] = -0.4
            enemyY[i] += enemychangey[i]
        elif enemyX[i] <= 0:
            enemychangex[i] = 0.4
            enemyY[i] += enemychangey[i]

        if bullet_state=='fire' and is_collision(enemyX[i], enemyY[i], setter, bulletY):
            collide_sound = mixer.Sound('catdead.wav')
            collide_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 100)
        villain(enemyX[i], enemyY[i],i)




    if bullet_state == "fire":
        fire_bullet(setter, bulletY)
        bulletY -= bulletchangeY
    if bullet_state == "fire" and bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    player(Xcoordinate, Ycoordinate)
    show_score(textx, texty)
    pygame.display.update()
