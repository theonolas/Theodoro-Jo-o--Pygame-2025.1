# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from random import *
from pygame.sprite import Group
import os
from os import path

pygame.init()

# ----- Gera tela principal
window = pygame.display.set_mode((500, 400))
pygame.display.set_caption('Py hunter!')

# ----- Inicia estruturas de dados
game = True

spritesheet = pygame.image.load("img/Quarble_8.webp").convert_alpha()

import pygame

def carregar_sprites(imagem_spritesheet, num_linhas, num_colunas):
    largura_sprite = imagem_spritesheet.get_width() // num_colunas
    altura_sprite = imagem_spritesheet.get_height() // num_linhas
    lista_sprites = []

    for linha in range(num_linhas):
        for coluna in range(num_colunas):
            pos_x = coluna * largura_sprite
            pos_y = linha * altura_sprite
            sprite = pygame.Surface((largura_sprite, altura_sprite), pygame.SRCALPHA)
            sprite.blit(imagem_spritesheet, (0, 0), pygame.Rect(pos_x, pos_y, largura_sprite, altura_sprite))
            lista_sprites.append(sprite)
    return lista_sprites


sprites = carregar_sprites(spritesheet, 7, 4)
sprites_nomeados = {}
for i in range(len(sprites)):
    nome = f"sprite{i+1}"
    sprites_nomeados[nome] = sprites[i]

sprites_morte= [sprites_nomeados['sprite1'],sprites_nomeados['sprite2'],sprites_nomeados['sprite3'],sprites_nomeados['sprite4']]
print(sprites_morte)

# ===== Loop principal =====
while game:
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Gera saídas
    window.fill((255, 255, 255))  # Preenche com a cor branca

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados