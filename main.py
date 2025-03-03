import pygame, sys
from game_manager import GameManager #Imports GameManager class
from ui import Button #Imports Button class

# Initialize Pygame
pygame.init()

# ==================== VARIABLE SETUP ==================== #
# == Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_TITLE = "Cell Wars"
GRID_SIZE = 20  # Number of cells in each dimension
CELL_SIZE = 20  # Size of each cell in pixels

# == Colors
BLACK = (34,35,35)
WHITE = (240, 246, 239)
GREEN = (0,255,0)

# == Font
font = pygame.font.Font("mondwest.ttf", 24)
title_font = pygame.font.Font("mondwest.ttf", 32)


# ==================== GAME SETUP ==================== #

# == Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# == Create the game manager
game_manager = GameManager(GRID_SIZE, GRID_SIZE, CELL_SIZE)
game_manager.initialize_players("Player 1", "Player 2")

# == Create move buttons
move_buttons = []
# ==== Player 1 buttons (left side)
for i in range(3):
    button_rect = pygame.Rect(50, 250 + i * 50, 130, 40)
    move_name = f"Move {i+1}"
    move_buttons.append(Button(button_rect, move_name, game_manager.players[0].color))

# ==== Player 2 buttons (right side)
for i in range(3):
    button_rect = pygame.Rect(SCREEN_WIDTH - 180, 250 + i * 50,130,40)
    move_name = f"Move {i+1}"
    move_buttons.append(Button(button_rect, move_name, game_manager.players[1].color))

# == Calculate grid coordinates from mouse position
grid_surface_width = GRID_SIZE * CELL_SIZE
grid_surface_height = GRID_SIZE * CELL_SIZE
grid_x = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
grid_y = (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) // 2

# ==================== FUNCTION DEFINITIONS ==================== #

def handle_input(mouse_pos, grid_x, grid_y, game_manager, move_buttons):
    """
    Handles user input and events.
    """

    # Calculate grid coordinates from mouse position
    mouse_grid_x = (mouse_pos[0] - grid_x) // CELL_SIZE
    mouse_grid_y = (mouse_pos[1] - grid_y) // CELL_SIZE

    # Checks and updates button hover state according to mouse position
    for button in move_buttons:
        button.hover = button.is_over(mouse_pos)

    # Handle events
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            return False, mouse_grid_x, mouse_grid_y
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Left click
            if event.button == 1 and not game_manager.game_over:
                # Check if a move button was clicked
                handle_button_click(move_buttons, mouse_pos, game_manager)

                # Check if grid was clicked and move was selected
                if game_manager.selected_move and (0 <= mouse_grid_x < GRID_SIZE and 0 <= mouse_grid_y < GRID_SIZE):
                    game_manager.apply_move(mouse_grid_x, mouse_grid_y)
                    # Clear button selection
                    for button in move_buttons:
                        button.selected = False

    return True, mouse_grid_x, mouse_grid_y

def handle_button_click(move_buttons, mouse_pos, game_manager):
    """
    Handles button clicks for move selection.
    """
    for i, button in enumerate(move_buttons):
        if button.is_over(mouse_pos):
            # Determine which player the button belongs to
            player_idx = i // 3 # This will be 0 if player 1 and 1 if player 2 (so clever)
            # Only allow current players button to be clicked
            if player_idx == game_manager.current_player_index:
                selected_move_name = f"Move {(i % 3) + 1}" # Modulo leaves the reminder of division, but if a < b it just equals b
                game_manager.select_move(selected_move_name)
                print(f"Selected Move {selected_move_name}")
                button.selected = True




def draw_player_infos(screen, game_manager, move_buttons, font):
    """
    Draws player's portraits, names, buttons and stats.
    """

    for i in range(2):
        next_player = game_manager.players[i]

        # Portrait Pos
        x_pos = 50 if i == 0 else SCREEN_WIDTH - 180

        # Portrait area
        portrait_rect = pygame.Rect(x_pos, 105, 130, 130)
        pygame.draw.rect(screen, next_player.color, portrait_rect)

        # Player name
        name_surface = font.render(next_player.name, True, WHITE)
        name_rect = name_surface.get_rect(center=(portrait_rect.centerx, portrait_rect.bottom - 160))
        screen.blit(name_surface, name_rect)

        # Player score
        score_text = f"Cells: {next_player.cells_conquered}"
        score_surface = font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center=(portrait_rect.centerx, portrait_rect.centery + 310))
        screen.blit(score_surface, score_rect)

        # Highlight current player
        if i == game_manager.current_player_index:
            pygame.draw.rect(screen, WHITE, portrait_rect.inflate(10,10), 3)

    for i, button in enumerate(move_buttons):
        button.draw(screen, font)


def draw_game_info(screen, game_manager, font, title_font):
    """
    Draw game information.
    When rendering text both _surface and _rect are needed.
    Surface is the image, and rect identifies where to put the image.
    """

    # Game title
    title_surface = title_font.render("Cell Wars", True, WHITE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
    screen.blit(title_surface, title_rect)

    # Turn counter
    turn_text = f"Turn: {game_manager.current_turn}/{game_manager.total_turns}"
    turn_surface = font.render(turn_text, True, WHITE)
    turn_rect = turn_surface.get_rect(center=(SCREEN_WIDTH // 2, 60))
    screen.blit(turn_surface, turn_rect)

    # Select starting cell indicator
    if game_manager.selected_move:
        move_text = "Select starting cell"
        move_surface = font.render(move_text, True, WHITE)
        move_rect = move_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        screen.blit(move_surface, move_rect)


def draw_game_over(screen, game_manager, title_font):
    """
    Draw game over message if the game is over.
    """

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
        game_over_surface = title_font.render(game_over_text, True, WHITE)
        text_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Background for text
        bg_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)
        pygame.draw.rect(screen, WHITE, bg_rect, 2)

        screen.blit(game_over_surface, text_rect)

def draw_grid(screen, game_manager, grid_x, grid_y, mouse_grid_x, mouse_grid_y):
    """
    Draw the center grid and cursor highlight.
    """
    grid_dimension = GRID_SIZE * CELL_SIZE

    #Draw Grid
    grid_surface = pygame.Surface((grid_dimension, grid_dimension))
    game_manager.grid.draw(grid_surface, BLACK)
    screen.blit(grid_surface, (grid_x, grid_y))

    # Draw cursor highlight if mouse is over the grid
    if (0 <= mouse_grid_x < GRID_SIZE and 0 <= mouse_grid_y < GRID_SIZE):
        highlight_rect = pygame.Rect(
            grid_x + mouse_grid_x * CELL_SIZE,
            grid_y + mouse_grid_y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, GREEN, highlight_rect, 2)


def render_game(screen, game_manager, font, title_font, move_buttons, grid_x, grid_y, mouse_grid_x, mouse_grid_y):
    """
    Render the game screen.
    """
    # Fill the screen
    screen.fill(BLACK)

    # Draw each component
    draw_grid(screen, game_manager, grid_x, grid_y, mouse_grid_x, mouse_grid_y)
    draw_player_infos(screen, game_manager, move_buttons, font)
    draw_game_info(screen, game_manager, font, title_font)
    draw_game_over(screen, game_manager, title_font)

    # Update the display
    pygame.display.flip()

# ==================== GAME LOOP ==================== #

running = True
mouse_grid_x, mouse_grid_y = 0,0

while running:
    # == Get Mouse position
    mouse_pos = pygame.mouse.get_pos()

    # == Handle input
    running, mouse_grid_x, mouse_grid_y = handle_input(mouse_pos, grid_x, grid_y, game_manager, move_buttons)

    # == Render game
    render_game(screen, game_manager, font, title_font, move_buttons, grid_x, grid_y, mouse_grid_x, mouse_grid_y)

# == Quit the game
pygame.quit()
sys.exit()









