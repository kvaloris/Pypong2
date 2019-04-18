import random
import sys
import pygame
from pygame.locals import *
import pygame.mixer

#initialisation de pygame
pygame.init()
fps = pygame.time.Clock()
#mise en place de la musique de fond
pygame.mixer.init()
pygame.mixer.music.load("sons/Musique.wav")
pygame.mixer.music.play(-1)
#création d'une variable pour les effets sonores
ball_coll= pygame.mixer.Sound("sons/flaunch.wav")

#création de la fenêtre pour le jeu
fenetre= pygame.display.set_mode((640, 480))
pygame.display.set_caption("pypong")
#mise en place des couleurs
BLACK= (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE= (255,255,255)


WIDTH = 640
HEIGHT = 480
BALL_RADIUS = 20
#création d'une variable pour la position
ball_pos = [0,0]
#création d'une variable pour la vitesse
ball_vel = [0,0]



PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
#définition de variables pour la vitesse des raquettes
paddle1_vel = 0
paddle2_vel = 0
#définition de variables pour la vitesse des raquettes
paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT//2]
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
score1=-1
score2=0
pause = False


#fonction qui permet de lancer la balle dans le jeu et retourne un vecteur position et un vecteur vitesse
#si right est vrai, lancer à droit, sinon à gauche
def ball_init(right):
    global ball_pos, ball_vel # ce sont des vecteur gardés comme listes 
    ball_pos = [WIDTH//2,HEIGHT//2]
    #définition d'une trajectoire aléatoire pour la balle
    values=[-5,-4, -3, -2, 2, 3, 4, 5]
    horz = random.choice(values)
    vert = random.choice(values)

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
        #définition d'une fonction qui contient tout le code graphique
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, score1, score2

    canvas.fill(BLACK)
    
    #mettre une image de fond
    image_fond = pygame.image.load("images/sky.jpg")
    fond = image_fond.convert()
    fenetre.blit(fond,(0,0))
    
    fenetre.blit(canvas, (0,0))
    #création des différents éléments graphique
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)
    #mise en place d'une police d'écriture
    font=pygame.font.SysFont('Calibri', 25, True, False)
    text=font.render("Score :" + str(score2), True, WHITE)
    #affichage du mot "score" à l'écran
    fenetre.blit(text, [130,0])
    #mise en place d'une police d'écriture
    font=pygame.font.SysFont('Calibri', 25, True, False)
    text=font.render("Score :"+ str(score1), True, WHITE)
    #affichage du mot "score" à l'écran
    fenetre.blit(text, [470,0])

     #mettre à jour la position de la raquette et garder la raquette dans la fenêtre
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

        #mise à jour de la balle
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #dessiner les raquettes et la balle
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    #collision de la balle avec les murs du haut et du bas
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        #lancement du son pour les collisions
        ball_coll.play()
        
        
    #collision de la balle avec les murs du haut et du bas    
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        #lancement du son pour les collisions
        ball_coll.play()

    #collision de la balle avec les raquettes
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.5
        ball_vel[1] *= 1.5
        #lancement du son pour les collisions
        ball_coll.play()
      

#définition du score
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
    
        ball_init(True)
        #augmentation du score à chaque but
        score1 += 1
    
    #collision de la balle avec les raquettes
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
        ball_coll.play()
#définition du score     
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
      
        ball_init(False)
        #augmentation du score à chaque but
        score2 += 1

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

#création de la fonction pause du programme
def paused(event):
    global pause
    #importation de la police 
    largeText = pygame.font.SysFont('Calibri', 100, True, False)
    #création du texte
    TextSurf,TextRect = text_objects("Pause", largeText)
    #centrage du texte
    TextRect.center = ((WIDTH//2), (HEIGHT//2))
    #affichage du texte
    fenetre.blit(TextSurf, TextRect)
    
    while pause:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #création d'une touche permettant d'annuler la pause du programme
            if event.key == K_l:
                pause = False
        pygame.display.update()
        fps.tick(15)
        
    


    #création de touches pour jouer au jeu
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
    

#keyup handler
#création de touches pour jouer au jeu
def keyup(event):
    global paddle1_vel, paddle2_vel, pause

    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0




#boucle du jeu
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
#mise à jour du jeu
    pygame.display.update()
    fps.tick(200)
