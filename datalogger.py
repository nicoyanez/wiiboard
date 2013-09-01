import pygame
from pygame.locals import *
import random

pygame.init()
pygame.display.set_mode((850,450))
pygame.display.set_caption("Grafico de acelerometro WiiMote")
screen = pygame.display.get_surface()
###########timer de refresco
pygame.time.set_timer(USEREVENT+1,1000)

circulos =0
while True:
    print circulos
    screen.fill((128,128,128))
    for i in range(circulos):
        pygame.draw.circle(screen,(255,255,255),(random.randint(0,600),random.randint(0,400)),random.randint(30,100),20)
    for event in pygame.event.get():
        if event.type == USEREVENT+1:
            print "##actualizaGrafico"
            circulos+=1
            pygame.display.flip()
        et = event.type
        if et == 12:
            pygame.display.quit()
