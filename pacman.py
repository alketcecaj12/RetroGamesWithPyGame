import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pacman")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Pacman properties
pacman_radius = 20
pacman_x = width // 2
pacman_y = height // 2
pacman_speed = 5

# Ghost properties
ghost_radius = 20
ghost_x = random.randint(0, width)
ghost_y = random.randint(0, height)
ghost_speed = 3

# Dot properties
dot_radius = 5
dots = [(random.randint(0, width), random.randint(0, height)) for _ in range(20)]

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move Pacman
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_x -= pacman_speed
    if keys[pygame.K_RIGHT]:
        pacman_x += pacman_speed
    if keys[pygame.K_UP]:
        pacman_y -= pacman_speed
    if keys[pygame.K_DOWN]:
        pacman_y += pacman_speed

    # Keep Pacman within the window
    pacman_x = max(pacman_radius, min(width - pacman_radius, pacman_x))
    pacman_y = max(pacman_radius, min(height - pacman_radius, pacman_y))

    # Move Ghost towards Pacman
    if ghost_x < pacman_x:
        ghost_x += ghost_speed
    elif ghost_x > pacman_x:
        ghost_x -= ghost_speed
    if ghost_y < pacman_y:
        ghost_y += ghost_speed
    elif ghost_y > pacman_y:
        ghost_y -= ghost_speed

    # Check for collision with dots
    for dot in dots[:]:
        if ((pacman_x - dot[0])**2 + (pacman_y - dot[1])**2)**0.5 < pacman_radius + dot_radius:
            dots.remove(dot)
            score += 10

    # Check for collision with ghost
    if ((pacman_x - ghost_x)**2 + (pacman_y - ghost_y)**2)**0.5 < pacman_radius + ghost_radius:
        running = False

    # Clear the screen
    window.fill(BLACK)

    # Draw Pacman
    pygame.draw.circle(window, YELLOW, (pacman_x, pacman_y), pacman_radius)

    # Draw Ghost
    pygame.draw.circle(window, BLUE, (int(ghost_x), int(ghost_y)), ghost_radius)

    # Draw dots
    for dot in dots:
        pygame.draw.circle(window, WHITE, dot, dot_radius)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()