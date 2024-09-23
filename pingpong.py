import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dy):
        self.rect.y += dy
        # Keep paddle within screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X * (-1 if random.choice([True, False]) else 1)
        self.speed_y = BALL_SPEED_Y * (-1 if random.choice([True, False]) else 1)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        # Reset ball if it goes out of bounds (left or right)
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            return True  # Indicates that the ball has gone out of bounds
        
        return False

# Main game function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Game")
    
    clock = pygame.time.Clock()
    
    # Create paddles and ball
    left_paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    left_score = 0
    right_score = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player controls for left paddle (W/S keys)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:
            left_paddle.move(PADDLE_SPEED)

        # Player controls for right paddle (UP/DOWN arrow keys)
        if keys[pygame.K_UP]:
            right_paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            right_paddle.move(PADDLE_SPEED)

        # Move the ball and check for scoring
        ball_out_of_bounds = ball.move()
        
        # Check for collision with paddles
        if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
            ball.speed_x *= -1
        
        # Check for scoring conditions
        if ball_out_of_bounds:
            if ball.rect.left <= 0:  
                right_score += 1  
            else:  
                left_score += 1  
            ball.__init__()  

        # Draw everything
        screen.fill(BLACK)  
        
        pygame.draw.rect(screen, WHITE, left_paddle.rect)  
        pygame.draw.rect(screen, WHITE, right_paddle.rect)  
        pygame.draw.ellipse(screen, WHITE, ball.rect)  

        # Draw scores
        font = pygame.font.Font(None, 74)
        score_text = font.render(f"{left_score} : {right_score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()  
        
        clock.tick(60)  

if __name__ == "__main__":
    main()