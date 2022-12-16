import pygame
import random
from pygame.locals import *
from sys import exit
import time

pygame.init()
largura = 975
altura = 720

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Mata Mosquito")

posicaoX = random.randint(0,880)
posicaoY = random.randint(0,600)


class mosca(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load("fly1.png"))
        self.sprites.append(pygame.image.load("fly2.png"))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (610//7, 511//7))
        self.rect = self.image.get_rect()
        self.rect.topleft = posicaoX, posicaoY

    def update(self):
        self.atual += 1
        if self.atual >= 2:
            self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (610//7, 511//7))
        self.rect = self.image.get_rect()
        self.rect.topleft = posicaoX, posicaoY
        time.sleep(0.1)
        


sprites = pygame.sprite.Group()
mosca = mosca()
sprites.add(mosca)
background_image = pygame.image.load("park_background.webp").convert()
background_image = pygame.transform.scale(background_image,(largura,altura))

while True:
    #tela.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            print(mouse)
            if mosca.rect.collidepoint(mouse):
                posicaoX = random.randint(0,880)
                posicaoY = random.randint(0,600)
                ultimo = pygame.time.get_ticks()/1000
            
    tela.blit(background_image,(0,0))
    sprites.draw(tela)
    #posicaoX = random.randint(0,880)
    #posicaoY = random.randint(0,600)
    sprites.update()
    pygame.display.flip()
