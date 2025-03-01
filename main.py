import pygame, sys
from grid import Grid # Imports Grid Class

# Initialize Pygame
pygame.init()

# Cons
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_TITLE = "Cell Wars"
GRID_SIZE = 20  # Number of cells in each dimension
CELL_SIZE = 20  # Size of each cell in pixels

# Style
BLACK = (34,35,35)
WHITE = (240, 246, 239)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Create the grid
grid = Grid(GRID_SIZE, GRID_SIZE, CELL_SIZE)

# Set some test cells
grid.set_cell(5, 5, Grid.PLAYER1)
grid.set_cell(10, 10, Grid.PLAYER2)

# Game Loop
running = True
while running:
    #Even handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Fill Screen
    screen.fill(BLACK)

    # Draw the grid
    grid_surface = pygame.Surface((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
    grid.draw(grid_surface, BLACK)

    # Center the grid on the screen
    grid_x = (SCREEN_WIDTH - grid_surface.get_width()) // 2
    grid_y = (SCREEN_HEIGHT - grid_surface.get_height()) // 2
    screen.blit(grid_surface, (grid_x, grid_y))

    #Update display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()