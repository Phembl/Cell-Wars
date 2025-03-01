import pygame, sys

# Initialize Pygame
pygame.init()

# Cons
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_TITLE = "Cell Wars"

# Style
BLACK = (34,35,35)
WHITE = (240, 246, 239)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Game Loop
running = True
while running:
    #Even handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Fill Screen
    screen.fill(BLACK)

    #Update display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()