import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Arkade Clone")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Paddle
paddle_width = 150
paddle_height = 20
paddle_x = screen_width // 2 - paddle_width // 2
paddle_y = screen_height - 40

# Ball
ball_radius = 10
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_dx = 5
ball_dy = -5

# Blocks
block_width = 70
block_height = 30
blocks = []

# Game variables
score = 0
lives = 3
game_state = "start"

# Fonts
font = pygame.font.Font(None, 36)

def create_blocks():
    for row in range(5):
        for col in range(10):
            block = pygame.Rect(col * (block_width + 5) + 15, row * (block_height + 5) + 50, block_width, block_height)
            color = random.choice(COLORS)
            blocks.append((block, color))

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_dx = random.choice([-5, 5])
    ball_dy = -5

create_blocks()

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state != "play":
                game_state = "play"
                if not blocks:
                    create_blocks()
                reset_ball()

    if game_state == "play":
        # Move paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= 7
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
            paddle_x += 7

        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with walls
        if ball_x <= ball_radius or ball_x >= screen_width - ball_radius:
            ball_dx *= -1
        if ball_y <= ball_radius:
            ball_dy *= -1

        # Ball collision with paddle
        if ball_y >= paddle_y - ball_radius and paddle_x < ball_x < paddle_x + paddle_width:
            ball_dy *= -1
            # Adjust angle based on where the ball hits the paddle
            ball_dx += (ball_x - (paddle_x + paddle_width / 2)) / 5
            ball_dx = max(min(ball_dx, 8), -8)  # Limit horizontal speed

        # Ball collision with blocks
        for block, color in blocks[:]:
            if block.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
                ball_dy *= -1
                blocks.remove((block, color))
                score += 10

        # Check for loss of life
        if ball_y >= screen_height:
            lives -= 1
            if lives > 0:
                reset_ball()
            else:
                game_state = "game_over"

        # Check for win
        if not blocks:
            game_state = "win"

    # Draw everything
    screen.fill(BLACK)
    
    # Draw paddle
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    
    # Draw ball
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)
    
    # Draw blocks
    for block, color in blocks:
        pygame.draw.rect(screen, color, block)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (screen_width - 100, 10))

    # Draw game state messages
    if game_state == "start":
        start_text = font.render("Press SPACE to start", True, WHITE)
        screen.blit(start_text, (screen_width // 2 - 100, screen_height // 2))
    elif game_state == "game_over":
        game_over_text = font.render("GAME OVER - Press SPACE to restart", True, WHITE)
        screen.blit(game_over_text, (screen_width // 2 - 180, screen_height // 2))
    elif game_state == "win":
        win_text = font.render("YOU WIN! Press SPACE to play again", True, WHITE)
        screen.blit(win_text, (screen_width // 2 - 180, screen_height // 2))

    # Update display
    pygame.display.flip()

    # Control game speed
    clock.tick(60)