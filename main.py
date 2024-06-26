import pygame
import random
import os
from tkinter import simpledialog

pygame.init()

relogio = pygame.time.Clock()
icone  = pygame.image.load("recursos/icone.png")
iron = pygame.image.load("recursos/iron.png")
fundo = pygame.image.load("recursos/fundo.png")
fundoStart = pygame.image.load("recursos/fundoStart.png")
fundoDead = pygame.image.load("recursos/fundoDead.png")
missel2 = pygame.image.load("recursos/missile2.png")
missel = pygame.image.load("recursos/missile.png")
cachorro = pygame.image.load("recursos/cachorro.png")
tamanho = (900,538)
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Iron Man do Marcão")
pygame.display.set_icon(icone)
missileSound = pygame.mixer.Sound("recursos/missile.wav")
explosaoSound = pygame.mixer.Sound("recursos/explosao.wav")
fonte = pygame.font.SysFont("comicsans",28)
fonteStart = pygame.font.SysFont("comicsans",55)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/ironsound.mp3")

branco = (255,255,255)
preto = (0, 0 ,0 )
amarelo = (255, 255, 0)


def jogar(nome):
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    posicaoXMissel2 = 500
    posicaoYMissel2 = -340
    velocidadeMissel = 1
    velocidadeMissel2 = 1
    pontos = 0
    larguraPersona = 100
    alturaPersona = 170
    larguaMissel  = 50
    alturaMissel  = 200
    larguaMissel2  = 50
    alturaMissel2  = 100
    dificuldade  = 20
    
    posicaoXCachorro = 0
    posicaoyCachorro = 450
    velocidadeCachorro = 3

    raio_sol = 50
    crescimento = 0.1
    max_crescimento = 5
    posicao_sol = (60, 110)  # Posição do sol (canto superior esquerdo)
    direcao_crescimento = 1

    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
                          
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 10
        elif posicaoXPersona >750:
            posicaoXPersona = 740
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 10
        elif posicaoYPersona > 473:
            posicaoYPersona = 463
        
        posicaoXCachorro += velocidadeCachorro
        if posicaoXCachorro > tamanho[0]:
            posicaoXCachorro = -200

           

        tela.fill(branco)
        tela.blit(fundo, (0, 0))
        tela.blit(iron, (posicaoXPersona, posicaoYPersona))
        tela.blit(cachorro, (posicaoXCachorro, 400))

        posicaoYMissel = posicaoYMissel + velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoXMissel = random.randint(0,400)
            pygame.mixer.Sound.play(missileSound)

        posicaoYMissel2 = posicaoYMissel2 + velocidadeMissel2
        if posicaoYMissel2 > 600:
            posicaoYMissel2 = -240
            pontos = pontos + 1
            velocidadeMissel2 = velocidadeMissel2 + 1
            posicaoXMissel2 = random.randint(400,800)
            pygame.mixer.Sound.play(missileSound)
            
            
        tela.blit( missel, (posicaoXMissel, posicaoYMissel) )
        tela.blit( missel2, (posicaoXMissel2, posicaoYMissel2) )
        
        texto = fonte.render(nome+"- Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (10,10))
      
        pygame.draw.circle(tela, amarelo, posicao_sol, int(raio_sol))

        raio_sol += crescimento * direcao_crescimento
        if raio_sol >= 50 + max_crescimento or raio_sol <= 50 - max_crescimento:
            direcao_crescimento *= -1

        

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguaMissel))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaMissel))
        pixelsMissel2X = list(range(posicaoXMissel2, posicaoXMissel2 + larguaMissel2))
        pixelsMissel2Y = list(range(posicaoYMissel2, posicaoYMissel2 + alturaMissel2))
        
        #print( len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )   )
        if  len( list( set(pixelsMisselY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                dead(nome, pontos)
            
        if  len( list( set(pixelsMissel2Y).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsMissel2X).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                dead(nome, pontos)
        
    
        
        pygame.display.update()
        relogio.tick(60)


def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    
    jogadas  = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt","w",encoding="utf-8")
        arquivo.close()
 
    jogadas[nome] = pontos   
    arquivo = open("historico.txt","w",encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (40,422,750,100),0)
        textoStart = fonteStart.render("RESTART", True, branco)
        tela.blit(textoStart, (400,452))
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (60,482))
        pygame.display.update()
        relogio.tick(60)


def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8" )
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass
    
    nomes = sorted(estrelas, key=estrelas.get,reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330,482))
        
        
        posicaoY = 50
        for key,nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - "+str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300,posicaoY))
            posicaoY = posicaoY + 30

            
        
        pygame.display.update()
        relogio.tick(60)


def start():
    nome = simpledialog.askstring("GTA","Nome Completo:")
    
    
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (105,422,750,100),0)
        buttonRanking = pygame.draw.rect(tela, preto, (35,50,200,50),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90,50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (380,422))

        
        
        pygame.display.update()
        relogio.tick(60)

start()

