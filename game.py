import pygame
import random
import sys
import os

# Começa o jogo
pygame.init()

# Constantes default
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Astro Jump")
clock = pygame.time.Clock()

#Classes
class Dinosaur:
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
        image_path = os.path.join('img', 'astronauta1.png')
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

class Cactus:
    def __init__(self):
        self.width = 20
        self.height = 40
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.speed = 5

    def update(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

def main():
    dinosaur = Dinosaur()
    cacti = []
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
                        # Reset game
                        dinosaur = Dinosaur()
                        cacti = []
                        score = 0
                        game_over = False
                    else:
                        dinosaur.jump()

        if not game_over:
            dinosaur.update()

            # faz aparecer o cactus
            if len(cacti) == 0 or cacti[-1].x < SCREEN_WIDTH - 300:
                if random.random() < 0.02:
                    cacti.append(Cactus())

            for cactus in cacti[:]:
                cactus.update()
                if cactus.x + cactus.width < 0:
                    cacti.remove(cactus)
                    score += 1

            # Colisão 
            for cactus in cacti:
                if (dinosaur.x < cactus.x + cactus.width and
                    dinosaur.x + dinosaur.width > cactus.x and
                    dinosaur.y < cactus.y + cactus.height and
                    dinosaur.y + dinosaur.height > cactus.y):
                    game_over = True

        # Desenha
        screen.fill(WHITE)
        
        # Chão
        pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        
        # Desenha o dinossauro
        dinosaur.draw()
        
        # Desenha o cactus
        for cactus in cacti:
            cactus.draw()

        # Desenha o score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over! Press SPACE to restart", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()