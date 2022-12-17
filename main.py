import pygame
import random
from pygame.locals import *
from sys import exit
import time


pygame.init()
# Definição da música do jogo e seu volume
pygame.mixer.music.set_volume(0.17)
musica_de_fundo = pygame.mixer.music.load("musica_fundo.ogg")
pygame.mixer.music.play(-1)
#musica_da_derrtota = pygame.mixer.music.load('/home/GabrielBastos/Área de trabalho/Jogo_versao2_ Algoritmos1_ufma/jogo-/smw_game_over.wav')


# aqui definimos a largura e a altura que vai ter a tela do jogo
largura = 975
altura = 720

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Mata Mosquito")

posicaoX = random.randint(0, 880)
posicaoY = random.randint(0, 600)
# Esse será o som que irá ser disparado a cada clique do mouse no sprite
songbotton = pygame.mixer.Sound("songbottom.wav")
# Essas são as definições da fonte que iremos usar para escrever os textos na tela
fonte = pygame.font.SysFont("arial", 40, True, False)

# Função para retornar uma tupla com dois valores randômicos, um para X e outro para Y


def posicaoRandomica():
    posicaoX = random.randint(0, 880)
    posicaoY = random.randint(0, 600)
    return (posicaoX, posicaoY)


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
        self.rect.topleft = nova_posicao

    def update(self):
        self.atual += 1
        if self.atual >= 2:
            self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (610//7, 511//7))
        self.rect = self.image.get_rect()
        self.rect.topleft = nova_posicao


nova_posicao = posicaoRandomica()
sprites = pygame.sprite.Group()
mosca = mosca()
sprites.add(mosca)
# Plano de fundo da tela e seu tamanho
background_image = pygame.image.load("background.webp").convert()
background_image = pygame.transform.scale(background_image, (largura, altura))
# definições iniciais do jogo
pontos = 0
ultimo_tempo = 0
vidas = 5
while True:
    #  Usando a forma de armazenar dados em arquivo, implementamos o highscore do jogo,
    #  onde para cada iteração é verificado se a pontuação do jogador é maior que o highscore
    with open("highscore.txt", "r") as highscore:
        for pontuação in highscore.readlines():
            highscore = pontuação
            if pontos > int(pontuação):
                with open("highscore.txt", "w") as maior_pontuação:
                    maior_pontuação.write(str(pontos))
    # textos que irão aparecer na tela
    mensagem_highscore = f"Highscore: {highscore}"
    mensagem_pontos = f"Pontos: {pontos}"
    mensagem_vidas = f"Vidas: {vidas}"
    texto_pontos_formatado = fonte.render(mensagem_pontos, False, (0, 0, 0))
    texto_highscore_formatado = fonte.render(
        mensagem_highscore, False, (0, 0, 0))
    texto_vidas_formatado = fonte.render(mensagem_vidas, False, (0, 0, 0))
    # pega o tempo em milisecundos a cada iteração e transforma para segundos
    tempo_inicial = pygame.time.get_ticks()/1000

    # verifica se as vidas do jogador acabaram, caso tenha acabado, o jogo termina
    if vidas == 0:
        print("Você perdeu")
        exit()
    # verifica se o intervalo entre o ultimo clique feito pelo jogador e o tempo corrido do momento é maior que 1.2 segundos,
    # caso seja, o sprite irá mudar randomicamente sua posição para outro local e o jogador perderá uma vida
    if tempo_inicial-ultimo_tempo >= 1.2:
        nova_posicao = posicaoRandomica()
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
                nova_posicao = posicaoRandomica()
                sprites.update()
                ultimo_tempo = pygame.time.get_ticks()/1000

    # posicionamento do plano de fundo
    tela.blit(background_image, (0, 0))
    sprites.draw(tela)
    tela.blit(texto_pontos_formatado, (737, 36))
    tela.blit(texto_highscore_formatado, (329, 36))
    tela.blit(texto_vidas_formatado, (52, 36))
    sprites.update()
    pygame.display.flip()
