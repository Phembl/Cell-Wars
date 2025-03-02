import pygame, sys
from grid import Grid # Imports Grid Class
from game_manager import GameManager #Imports GameManager class


# Initialize Pygame
pygame.init()

# Cons
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_TITLE = "Cell Wars"
GRID_SIZE = 20  # Number of cells in each dimension
CELL_SIZE = 20  # Size of each cell in pixels

# -- Style
# Colors
BLACK = (34,35,35)
WHITE = (240, 246, 239)
GREEN = (0,255,0)
# Font
font = pygame.font.Font("mondwest.ttf", 24)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Create the game manager
game_manager = GameManager(GRID_SIZE, GRID_SIZE, CELL_SIZE)
game_manager.initialize_players("Player 1", "Player 2")

# Game Loop
running = True
while running:
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Calculate grid coordinates from mouse position
    grid_surface_width = GRID_SIZE * CELL_SIZE
    grid_surface_height = GRID_SIZE * CELL_SIZE
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
            if event.button == 1 and not game_manager.game_over:
                # Ensure mouse is within grid
                if (0 <= mouse_grid_x < GRID_SIZE and
                    0 <= mouse_grid_y < GRID_SIZE):

                    # Temporarily select a "default" move
                    game_manager.select_move("default")
                    game_manager.apply_move(mouse_grid_x, mouse_grid_y)

    #Fill Screen
    screen.fill(BLACK)

    # Draw the grid
    grid_surface = pygame.Surface((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
    game_manager.grid.draw(grid_surface, BLACK)

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

    # UI Infos
    # -- Current player
    current_player = game_manager.get_current_player()
    player_text = f"Current Player: {current_player.name}"
    player_surface = font.render(player_text, True, WHITE)
    screen.blit(player_surface, (20, 20))

    # -- Turn counter
    turn_text = f"Turn: {game_manager.current_turn}/{game_manager.total_turns}"
    turn_surface = font.render(turn_text, True, WHITE)
    screen.blit(turn_surface, (20, 50))

    # -- Score
    # -- Player 1
    player1 = game_manager.players[0]
    score_text1 = f"{player1.name}: {player1.cells_conquered} cells"
    score_surface1 = font.render(score_text1, True, player1.color)
    screen.blit(score_surface1, (SCREEN_WIDTH - 200, 20))

    # -- Player 2
    player2 = game_manager.players[1]
    score_text2 = f"{player2.name}: {player2.cells_conquered} cells"
    score_surface2 = font.render(score_text2, True, player2.color)
    screen.blit(score_surface2, (SCREEN_WIDTH - 200, 50))

    # Game over message
    if game_manager.game_over:
        # Determine winner
        player1, player2 = game_manager.players
        if player1.cells_owned > player2.cells_owned:
            winner = player1.name
        elif player2.cells_owned > player1.cells_owned:
            winner = player2.name
        else:
            winner = "Draw"

        game_over_text = f"Game Over! Winner: {winner}"
        game_over_surface = font.render(game_over_text, True, WHITE)
        text_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(game_over_surface, text_rect)

    #Update display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()