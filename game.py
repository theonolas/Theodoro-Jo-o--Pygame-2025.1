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
        
        # Load and scale the astronaut image
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


def main():
    dinosaur = Dinosaur()
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
                        score = 0
                        game_over = False
                    else:
                        dinosaur.jump()

        if not game_over:
            # Update
            dinosaur.update()


        # Draw
        screen.fill(WHITE)
        
        # Draw ground
        pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        
        # Draw dinosaur
        dinosaur.draw()
        

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over! Press SPACE to restart", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()