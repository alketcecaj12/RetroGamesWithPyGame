import pygame
import random

# Inizializzazione di Pygame
pygame.init()

# Colori
BIANCO = (255, 255, 255)
NERO = (0, 0, 0)
ROSSO = (255, 0, 0)
VERDE = (0, 255, 0)

# Dimensioni della finestra
LARGHEZZA = 800
ALTEZZA = 600

# Dimensioni del serpente e della mela
DIMENSIONE_BLOCCO = 20

# Velocità del gioco
FPS = 6

# Creazione della finestra
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption('Gioco del Serpente che piace a Enea! ')

# Funzione per disegnare il serpente
def disegna_serpente(serpente):
    for blocco in serpente:
        pygame.draw.rect(schermo, VERDE, [blocco[0], blocco[1], DIMENSIONE_BLOCCO, DIMENSIONE_BLOCCO])

# Funzione principale del gioco
def gioco():
    game_over = False
    game_chiuso = False

    # Posizione iniziale del serpente
    x = LARGHEZZA / 2
    y = ALTEZZA / 2

    # Velocità iniziale del serpente
    x_change = 0
    y_change = 0

    # Corpo del serpente
    serpente = []
    lunghezza_serpente = 1

    # Posizione della mela
    mela_x = round(random.randrange(0, LARGHEZZA - DIMENSIONE_BLOCCO) / DIMENSIONE_BLOCCO) * DIMENSIONE_BLOCCO
    mela_y = round(random.randrange(0, ALTEZZA - DIMENSIONE_BLOCCO) / DIMENSIONE_BLOCCO) * DIMENSIONE_BLOCCO

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_chiuso = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -DIMENSIONE_BLOCCO
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = DIMENSIONE_BLOCCO
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -DIMENSIONE_BLOCCO
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = DIMENSIONE_BLOCCO
                    x_change = 0

        # Aggiornamento della posizione del serpente
        x += x_change
        y += y_change

        # Wrap-around: attraversamento dei bordi
        if x >= LARGHEZZA:
            x = 0
        elif x < 0:
            x = LARGHEZZA - DIMENSIONE_BLOCCO
        if y >= ALTEZZA:
            y = 0
        elif y < 0:
            y = ALTEZZA - DIMENSIONE_BLOCCO

        schermo.fill(NERO)

        # Disegno della mela
        pygame.draw.rect(schermo, ROSSO, [mela_x, mela_y, DIMENSIONE_BLOCCO, DIMENSIONE_BLOCCO])

        testa_serpente = []
        testa_serpente.append(x)
        testa_serpente.append(y)
        serpente.append(testa_serpente)

        if len(serpente) > lunghezza_serpente:
            del serpente[0]

        # Controllo collisione con se stesso
        for segmento in serpente[:-1]:
            if segmento == testa_serpente:
                game_over = True

        disegna_serpente(serpente)

        pygame.display.update()

        # Controllo se il serpente mangia la mela
        if x == mela_x and y == mela_y:
            mela_x = round(random.randrange(0, LARGHEZZA - DIMENSIONE_BLOCCO) / DIMENSIONE_BLOCCO) * DIMENSIONE_BLOCCO
            mela_y = round(random.randrange(0, ALTEZZA - DIMENSIONE_BLOCCO) / DIMENSIONE_BLOCCO) * DIMENSIONE_BLOCCO
            lunghezza_serpente += 1

        clock.tick(FPS)

    pygame.quit()

# Avvio del gioco
gioco()