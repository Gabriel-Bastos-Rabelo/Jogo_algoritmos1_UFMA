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


# aqui definimos a largura e a altura que vai ter a tela do jogo
largura = 975
altura = 720

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Mata Mosquito")


# Esse será o som que irá ser disparado a cada clique do mouse no sprite
songbotton = pygame.mixer.Sound("songbottom.wav")
# Essas são as definições da fonte que iremos usar para escrever os textos na tela
fonte = pygame.font.SysFont("arial", 40, True, False)

# Função para retornar uma tupla com dois valores randômicos, um para X e outro para Y
def posicaoRandomica():
    posicaoX = random.randint(0, 880)
    posicaoY = random.randint(0, 600)
    return (posicaoX, posicaoY)


class Game(pygame.sprite.Sprite):
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
        self.fonte = pygame.font.match_font('arial')
        self.tela = pygame.display.set_mode((largura, altura))
        self.relogio = pygame.time.Clock()
        self.esta_rodando = True
        
    # Definimos um método para trocar as imagens da mosca a cada iteração no loop principal para dar o 
    # efeito que ela está voando
    def update(self):
        self.atual += 1
        if self.atual >= 2:
            self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (610//7, 511//7))
        self.rect = self.image.get_rect()
        self.rect.topleft = nova_posicao
   
    
    # Método criado para exibir textos na tela inicial e na tela final
    def mostrar_texto(self, texto, tamanho, cor, x, y):
        fonte = pygame.font.Font(self.fonte, tamanho)
        texto = fonte.render(texto, True, cor)
        texto_rect = texto.get_rect()
        texto_rect.midtop = (x,y)
        self.tela.blit(texto, texto_rect)
    
    # Método para implementar uma tela de start
    def mostrar_tela_start(self):
        self.mostrar_texto("Pressione espaço para jogar", 32, (244,233,51), largura/2, 320)
        self.mostrar_texto("Desenvolvido por Gabriel Bastos e João Felipe", 19, (255,255,255), largura/2, 683)
        pygame.display.flip()
        self.esperar_por_jogador_start()
    
    # Método para implementar a escolha de nível
    def mostrar_tela_nivel(self):
        self.tela.fill((0,0,0))
        self.mostrar_texto("Escolha um nível para jogar", 32, (244,233,51), largura/2, 50)
        self.mostrar_texto("Pressione 1 para nível fácil", 25, (255,255,255), largura/2, 100)
        self.mostrar_texto("Pressione 2 para nível médio", 25, (255,255,255), largura/2, 140)
        self.mostrar_texto("Pressione 3 para nível difícil", 25, (255,255,255), largura/2, 180)
        pygame.display.flip()
        nivel = self.esperar_por_jogador_nivel()
        return nivel

    # Método para implementar uma tela de game over
    def mostrar_tela_derrota(self):
        self.tela.fill((0,0,0))
        self.mostrar_texto("Você perdeu", 32, (244,233,51), largura/2, 320)
        self.mostrar_texto("Aperte espaço para reiniciar o jogo", 19, (255,255,255), largura/2, 654)
        self.mostrar_texto("Aperte backspace para sair do jogo", 19, (255,255,255), largura/2, 683)
        pygame.display.flip()
        reinicio = self.esperar_por_jogador_start()
        return reinicio
    
    # Método para esperar pela ação do jogador na tela de start
    def esperar_por_jogador_start(self):
        esperando = True
        recomeço = False
        while esperando:
            self.relogio.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.esta_rodando = False
                    exit()
                if event.type == pygame.KEYUP:
                    if event.key == K_SPACE:
                        esperando = False
                        recomeço = True
                        return recomeço
                    elif event.key == K_BACKSPACE:
                        return recomeço
   
    # Método para esperar a entrada do jogador com o nível que ele deseja
    def esperar_por_jogador_nivel(self):
        while True:
            self.relogio.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYUP:
                    if event.key == K_1:
                        return 1.3
                    elif event.key == K_2:
                        return 1.1
                    elif event.key == K_3:
                        return 0.8


                        

nova_posicao = posicaoRandomica()
sprites = pygame.sprite.Group()
Game = Game()
Game.mostrar_tela_start()
sprites.add(Game)
Game.mostrar_tela_nivel()
nivel = Game.mostrar_tela_nivel()
# Plano de fundo da tela e seu tamanho
background_image = pygame.image.load("background.webp").convert()
background_image = pygame.transform.scale(background_image, (largura, altura))
# definições iniciais do jogo
pontos = 0
ultimo_tempo = 0
vidas = 5
primeiro_loop = True

# Concatenação de strings para gerar nome do arquivo necessário para leitura do highscore
lista = ["highscore", str(nivel), ".txt"]
arquivo_nivel = "".join(lista)

while True:
    #  Usando a forma de armazenar dados em arquivo, implementamos o highscore do jogo,
    #  onde para cada iteração é verificado se a pontuação do jogador é maior que o highscore
    with open(arquivo_nivel, "r") as highscore:
        for pontuação in highscore.readlines():
            highscore = pontuação
            if pontos > int(pontuação):
                with open(arquivo_nivel, "w") as maior_pontuação:
                    maior_pontuação.write(str(pontos))
   
    # textos que irão aparecer na tela
    mensagem_highscore = f"Highscore: {highscore}"
    mensagem_pontos = f"Pontos: {pontos}"
    mensagem_vidas = f"Vidas: {vidas}"
    texto_pontos_formatado = fonte.render(mensagem_pontos, False, (0, 0, 0))
    texto_highscore_formatado = fonte.render(mensagem_highscore, False, (0, 0, 0))
    texto_vidas_formatado = fonte.render(mensagem_vidas, False, (0, 0, 0))
   
    # Verifica se é a primeira iteração no loop, para assim o último tempo não ser considerado 0
    if vidas==5 and primeiro_loop==True:
        ultimo_tempo = pygame.time.get_ticks()/1000
        primeiro_loop = False
    
    # Captura a cada iteração o tempo corrido do jogo
    tempo_corrente = pygame.time.get_ticks()/1000
    
    
    # verifica se as vidas do jogador acabaram, caso tenha acabado, o jogo será finalizado ou reinicializado pelo jogador
    if vidas == 0:
        resultado = Game.mostrar_tela_derrota()
        if resultado:
            vidas = 5
            pontos = 0
            primeiro_loop = True
        else:
            exit()
   
    # verifica se o intervalo entre o ultimo clique feito pelo jogador e o tempo corrido do momento é maior que 1.2 segundos,
    # caso seja, o sprite irá mudar randomicamente sua posição para outro local e o jogador perderá uma vida
    if tempo_corrente-ultimo_tempo >= nivel:
        nova_posicao = posicaoRandomica()
        sprites.update()
        ultimo_tempo = tempo_corrente
        vidas -= 1
    
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
            # caso a posição de clique do mouse colida com o retângulo gerado pelo sprite, os comandos abaixo serão executados
            # O sprite mudará sua posição randomicamente e o ultimo tempo vai ser atualizado
            if Game.rect.collidepoint(mouse):
                songbotton.play()
                pontos += 1
                nova_posicao = posicaoRandomica()
                sprites.update()
                ultimo_tempo = pygame.time.get_ticks()/1000

    # posicionamento do plano de fundo, posicionamento dos textos e atualização
    tela.blit(background_image, (0, 0))
    sprites.draw(tela)
    tela.blit(texto_pontos_formatado, (737, 36))
    tela.blit(texto_highscore_formatado, (329, 36))
    tela.blit(texto_vidas_formatado, (52, 36))
    sprites.update()
    pygame.display.flip()
