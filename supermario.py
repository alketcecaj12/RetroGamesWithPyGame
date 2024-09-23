import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(50, SCREEN_HEIGHT - 150, 50, 50)
        self.velocity_y = 0
        self.on_ground = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        
        # Gravity
        if not self.on_ground:
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y
        
        # Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
        
        # Check for ground collision
        if self.rect.y >= SCREEN_HEIGHT - 50:  # Ground level
            self.rect.y = SCREEN_HEIGHT - 50
            self.on_ground = True
            self.velocity_y = 0
        else:
            self.on_ground = False

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.direction = random.choice([-1, 1])  # Random initial direction

    def move(self):
        self.rect.x += self.direction * 3
        
        # Change direction when hitting screen edges
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - 40:
            self.direction *= -1

# Coin class
class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)

# Main game function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Enhanced Mario Game")
    
    clock = pygame.time.Clock()
    player = Player()
    
    # Create platforms and collectibles
    platforms = [pygame.Rect(100 * i, SCREEN_HEIGHT - (i % 3) * 100 - 50, 100, 10) for i in range(8)]
    enemies = [Enemy(random.randint(200, SCREEN_WIDTH - 60), SCREEN_HEIGHT - random.randint(100, 200)) for _ in range(3)]
    coins = [Coin(random.randint(100, SCREEN_WIDTH - 20), random.randint(100, SCREEN_HEIGHT - 200)) for _ in range(5)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update player movement and check collisions with platforms
        player.move()
        
        # Check collision with platforms
        for platform in platforms:
            if player.rect.colliderect(platform) and not player.on_ground:
                player.rect.y = platform.top - player.rect.height
                player.on_ground = True
                player.velocity_y = 0
        
        # Draw everything
        screen.fill(WHITE) 

        # Draw platforms and collectibles
        for platform in platforms:
            pygame.draw.rect(screen, GREEN, platform)  
        
        for coin in coins:
            pygame.draw.rect(screen, YELLOW, coin.rect)  

        # Draw enemies
        for enemy in enemies:
            enemy.move()
            pygame.draw.rect(screen, RED, enemy.rect)

        # Draw player character
        pygame.draw.rect(screen, (0, 0, 255), player.rect)  
        
        pygame.display.flip()  
        
        clock.tick(60)  

if __name__ == "__main__":
    main()