import pygame
import random
from pygame.locals import *
from sys import exit
import time
from pydub import AudioSegment

pygame.init()
largura = 975
altura = 720

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Mata Mosquito")

posicaoX = random.randint(0, 880)
posicaoY = random.randint(0, 600)

songbotton = pygame.mixer.Sound("smw_shell_ricochet.wav")
fonte = pygame.font.SysFont("arial", 40, True, False)

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
        # time.sleep(0.1)


sprites = pygame.sprite.Group()
mosca = mosca()
sprites.add(mosca)
background_image = pygame.image.load("park_background.webp").convert()
background_image = pygame.transform.scale(background_image, (largura, altura))
# definições do jogo
pontos = 0
ultimo_tempo = 0
vidas = 5
while True:
    # textos que irão aparecer na tela
    mensagem_pontos = f"Pontos: {pontos}"
    mensagem_vidas = f"Vidas: {vidas}"
    texto_pontos_formatado = fonte.render(mensagem_pontos, False, (0,0,0))
    texto_vidas_formatado = fonte.render(mensagem_vidas, False, (0,0,0))
    # pega o tempo em milisecundos a cada iteração e transforma para segundos
    tempo_inicial = pygame.time.get_ticks()/1000

    # verifica se as vidas do jogador acabaram, caso tenha acabado, o jogo termina
    if vidas <= 0:
        print("Você perdeu")
        exit()
    # verifica se o intervalo entre o ultimo clique feito pelo jogador e o tempo corrido do momento é maior que 1.2 segundos,
    # caso seja, o sprite irá mudar randomicamente sua posição para outro local
    if tempo_inicial-ultimo_tempo >= 1.2:
        posicaoX = random.randint(0, 880)
        posicaoY = random.randint(0, 660)
        sprites.update()
        ultimo_tempo = tempo_inicial
        vidas -= 1
        print(vidas)
    # verifica todos os eventos do teclado capturados
    for event in pygame.event.get():
        # caso o evento capturado seja o de fechar o jogo, o jogo será encerrado
        if event.type == QUIT:
            pygame.quit()
            exit()
        # caso o evento seja de clique do mouse, verificaremos se o clique colidiu com o sprite
        elif event.type == pygame.MOUSEBUTTONUP:
            # primeiramente devemos pegar a posição de clique do mouse
            mouse = pygame.mouse.get_pos()
            print(mouse)
            # caso a posição de clique do mouse colida com o retângulo gerado pelo sprite, os comandos abaixo serão executados
            # O sprite mudará sua posição randomicamente e o ultimo tempo vai ser atualizado
            if mosca.rect.collidepoint(mouse):
                songbotton.play()
                pontos += 1
                print(pontos)
                posicaoX = random.randint(0, 880)
                posicaoY = random.randint(0, 600)
                sprites.update()
                ultimo_tempo = pygame.time.get_ticks()/1000
                continue

    tela.blit(background_image, (0, 0))
    sprites.draw(tela)
    #posicaoX = random.randint(0,880)
    #posicaoY = random.randint(0,600)
    tela.blit(texto_pontos_formatado, (737, 36))
    tela.blit(texto_vidas_formatado, (52, 44))
    sprites.update()
    pygame.display.flip()
