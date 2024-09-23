import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

COLORS = [CYAN, YELLOW, MAGENTA, RED, GREEN, BLUE, ORANGE]

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = COLORS[SHAPES.index(self.shape)]
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
        self.shape = list(zip(*self.shape[::-1]))

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid

def draw_grid(surface, grid):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            pygame.draw.rect(surface, grid[i][j], (j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    
    for i in range(GRID_HEIGHT + 1):
        pygame.draw.line(surface, WHITE, (0, i*BLOCK_SIZE), (GRID_WIDTH*BLOCK_SIZE, i*BLOCK_SIZE))
    for j in range(GRID_WIDTH + 1):
        pygame.draw.line(surface, WHITE, (j*BLOCK_SIZE, 0), (j*BLOCK_SIZE, GRID_HEIGHT*BLOCK_SIZE))

def draw_tetromino(surface, tetromino):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, tetromino.color, 
                    ((tetromino.x + j) * BLOCK_SIZE, (tetromino.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def valid_move(tetromino, grid):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                if tetromino.x + j < 0 or tetromino.x + j >= GRID_WIDTH or \
                   tetromino.y + i >= GRID_HEIGHT or \
                   grid[tetromino.y + i][tetromino.x + j] != BLACK:
                    return False
    return True

def clear_rows(grid, locked):
    inc = 0
    for i in range(GRID_HEIGHT - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            ind = i
            for j in range(GRID_WIDTH):
                try:
                    del locked[(j, i)]
                except:
                    continue
    
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    
    return inc

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    current_piece = Tetromino(GRID_WIDTH // 2 - 1, 0)
    next_piece = Tetromino(GRID_WIDTH // 2 - 1, 0)
    locked_positions = {}
    grid = create_grid(locked_positions)

    fall_time = 0
    fall_speed = 0.5
    level_time = 0
    score = 0

    running = True
    while running:
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_move(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                for i, row in enumerate(current_piece.shape):
                    for j, cell in enumerate(row):
                        if cell:
                            locked_positions[(current_piece.x + j, current_piece.y + i)] = current_piece.color
                current_piece = next_piece
                next_piece = Tetromino(GRID_WIDTH // 2 - 1, 0)
                score += clear_rows(grid, locked_positions) * 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_move(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_move(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_move(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_move(current_piece, grid):
                        current_piece.rotate()
                        current_piece.rotate()
                        current_piece.rotate()

        grid = create_grid(locked_positions)

        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_tetromino(screen, current_piece)
        pygame.display.update()

        if not valid_move(current_piece, grid):
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()