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
GREEN = (0,255,0)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Create the grid
grid = Grid(GRID_SIZE, GRID_SIZE, CELL_SIZE)

# TESTING
# -- Set some test cells
grid.set_cell(5, 5, Grid.PLAYER1)
grid.set_cell(10, 10, Grid.PLAYER2)

# -- Current player (for testing)
current_player = Grid.PLAYER1

# Game Loop
running = True
while running:
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Calculate grid coordinates from mouse position
    grid_x = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
    grid_y = (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) // 2

    mouse_grid_x = (mouse_pos[0] - grid_x) // CELL_SIZE
    mouse_grid_y = (mouse_pos[1] - grid_y) // CELL_SIZE

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Left click
            if event.button == 1:
                # Ensure mouse is within grid
                if (0 <= mouse_grid_x < GRID_SIZE and
                        0 <= mouse_grid_y < GRID_SIZE):
                    grid.set_cell(mouse_grid_x, mouse_grid_y, current_player)
                    # Switch player for testing
                    current_player = Grid.PLAYER2 if current_player == Grid.PLAYER1 else Grid.PLAYER1

    #Fill Screen
    screen.fill(BLACK)

    # Draw the grid
    grid_surface = pygame.Surface((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
    grid.draw(grid_surface, BLACK)

    # Center the grid on the screen
    screen.blit(grid_surface, (grid_x, grid_y))

    # Draw cursor highlight if mouse is over the grid
    if (0 <= mouse_grid_x < GRID_SIZE and
        0 <= mouse_grid_y < GRID_SIZE):
        highlight_rect = pygame.Rect(
            grid_x + mouse_grid_x * CELL_SIZE,
            grid_y + mouse_grid_y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, GREEN, highlight_rect, 2)

    #Update display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()