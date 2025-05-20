import pygame
import random
import sys
import os

# Inicia o Pygame
pygame.init()

# Constantes da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Astro Jump")
clock = pygame.time.Clock()

# Classe do botão
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Classe do astronauta
class Astronaut:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - 60
        self.width = 40
        self.height = 60
        self.jumping = False
        self.jump_velocity = 0
        self.gravity = 1
        self.jump_power = -20

        # Imagem do astronauta
        image_path = os.path.join('../img', 'astronauta1.png')
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def jump(self):
        if not self.jumping:
            self.jump_velocity = self.jump_power
            self.jumping = True

    def update(self):
        if self.jumping:
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity

            if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
                self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
                self.jumping = False
                self.jump_velocity = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Classe do satélite (obstáculo)
class Satellite:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.speed = 5

        # Imagem do satélite
        image_path = os.path.join('../img', 'Satelite.png')
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update(self):
        self.x -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Tela do menu principal
def show_menu():
    start_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50, 200, 50, "Iniciar Jogo", BLUE)
    instructions_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 50, "Instruções", BLUE)
    back_button = None

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button and back_button.is_clicked(event.pos):
                    return "menu"
                if start_button.is_clicked(event.pos):
                    return "start"
                if instructions_button.is_clicked(event.pos):
                    back_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Voltar", BLUE)
                    return "instructions"

        if back_button:
            back_button.draw()
            font = pygame.font.Font(None, 36)
            instructions = [
                "Como jogar:",
                "Pressione ESPAÇO para o astronauta pular",
                "Evite os satélites",
                "Você ganha pontos ao passar por cada satélite",
                "Fim de jogo ao colidir com um satélite",
                "Pressione ESPAÇO para reiniciar após perder"
            ]
            for i, line in enumerate(instructions):
                text = font.render(line, True, BLACK)
                screen.blit(text, (50, 50 + i * 40))
        else:
            start_button.draw()
            instructions_button.draw()
            font = pygame.font.Font(None, 74)
            title = font.render("Astro Jump", True, BLACK)
            screen.blit(title, (SCREEN_WIDTH//2 - 150, 50))

        pygame.display.flip()
        clock.tick(FPS)

# Função principal do jogo
def game_loop():
    astronaut = Astronaut()
    satellites = []
    score = 0
    game_over = False
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        astronaut = Astronaut()
                        satellites = []
                        score = 0
                        game_over = False
                    else:
                        astronaut.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    return  # Volta ao menu

        if not game_over:
            astronaut.update()

            # Gera novos satélites
            if len(satellites) == 0 or satellites[-1].x < SCREEN_WIDTH - 300:
                if random.random() < 0.02:
                    satellites.append(Satellite())

            for satellite in satellites[:]:
                satellite.update()
                if satellite.x + satellite.width < 0:
                    satellites.remove(satellite)
                    score += 1

            # Verifica colisão
            for satellite in satellites:
                if (astronaut.x < satellite.x + satellite.width and
                    astronaut.x + astronaut.width > satellite.x and
                    astronaut.y < satellite.y + satellite.height and
                    astronaut.y + astronaut.height > satellite.y):
                    game_over = True

        # Tela do jogo
        screen.fill(WHITE)

        # Chão
        pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

        # Astronauta
        astronaut.draw()

        # Satélites
        for satellite in satellites:
            satellite.draw()

        # Pontuação
        score_text = font.render(f"Pontuação: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Fim de Jogo! Clique para voltar ao menu", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

# Loop principal
def main():
    while True:
        menu_action = show_menu()

        if menu_action == "start":
            game_loop()
        elif menu_action == "instructions":
            show_menu()
        elif menu_action == "menu":
            continue

if __name__ == "__main__":
    main()