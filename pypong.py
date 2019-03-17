import random
import sys
import pygame
from pygame.locals import *
import pygame.mixer


pygame.init()
fps = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load("sons/Musique.wav")
pygame.mixer.music.play(-1)

ball_coll= pygame.mixer.Sound("sons/flaunch.wav")


fenetre= pygame.display.set_mode((640, 480))
pygame.display.set_caption("pypong")
BLACK= (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE= (255,255,255)


WIDTH = 640
HEIGHT = 480
BALL_RADIUS = 20
ball_pos = [0,0]
ball_vel = [0,0]



PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT//2]
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
score1=-1
score2=0
pause = False


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH//2,HEIGHT//2]
    horz = random.randrange(-5,5)
    vert = random.randrange(-5,5)
    if vert==0:
        vert += random.randrange(3,5)
    if horz==0:
        horz += random.randrange(3,4)
    
#    if right == False:
#        horz = - horz
# le - permet de faire partir la balle dans une autre direction
    ball_vel = [horz,vert]

    # define event handlers
    #permet d'activer ou d'arrêter le jeu
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)

#draw function of canvas
        #contient tout le code graphique
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, score1, score2

    canvas.fill(BLACK)
    
    image_fond = pygame.image.load("images/sky.jpg")
    fond = image_fond.convert()
    fenetre.blit(fond,(0,0))
    
    fenetre.blit(canvas, (0,0))
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)
    
    font=pygame.font.SysFont('Calibri', 25, True, False)
    text=font.render("Score :" + str(score2), True, WHITE)
    fenetre.blit(text, [130,0])
    
    font=pygame.font.SysFont('Calibri', 25, True, False)
    text=font.render("Score :"+ str(score1), True, WHITE)
    fenetre.blit(text, [470,0])

     # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel

    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

        #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #draw paddles and ball
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        ball_coll.play()
        
        
        
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        ball_coll.play()

    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.5
        ball_vel[1] *= 1.5
        ball_coll.play()
      


    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
    
        ball_init(True)
        score1 += 1
    

    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
        ball_coll.play()
        
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
      
        ball_init(False)
        score2 += 1
   
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def paused(event):
    global pause
    largeText = pygame.font.SysFont('Calibri', 100, True, False)
    TextSurf,TextRect = text_objects("Pause", largeText)
    TextRect.center = ((WIDTH//2), (HEIGHT//2))
    fenetre.blit(TextSurf, TextRect)
    #pygame.time.delay(0)
    
    while pause:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.key == K_l:
                pause = False
                #pygame.time.delay(
        pygame.display.update()
        fps.tick(15)
        
    


    #keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel, pause

    if event.key == K_UP:
        paddle2_vel = -8
        
    elif event.key == K_DOWN:
        paddle2_vel = 8
        
    elif event.key == K_w:
        paddle1_vel = -8
      
    elif event.key == K_s:
        paddle1_vel = 8
      
    elif event.key == K_p:
        pause = True
        paused(event)
        #while True:
            #keyup(event)
            
    

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel, pause

    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0
    #elif event.key == K_p:
        #pause = True
        #paused(event)
        #if keydown(event)=True:
            #pause=False




#game loop
while True:

    draw(fenetre)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)

        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps.tick(200)

#Score, sons, image de fond