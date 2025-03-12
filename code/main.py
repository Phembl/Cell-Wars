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
font = pygame.font.Font("font/mondwest.ttf", 24)
title_font = pygame.font.Font("font/mondwest.ttf", 32)
button_font = pygame.font.Font("font/mondwest.ttf", 18)

# == Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)


# ==================== FUNCTION DEFINITIONS ==================== #

def handle_input(mouse_pos, grid_x, grid_y, game_manager, action_buttons):
    """
    Handles user input and events.
    Returns True if the game is still running and grid coordinates.
    """

    # Calculate grid coordinates from mouse position
    mouse_grid_x = (mouse_pos[0] - grid_x) // CELL_SIZE
    mouse_grid_y = (mouse_pos[1] - grid_y) // CELL_SIZE

    # Checks and updates button hover state according to mouse position
    for button in action_buttons:
        button.hover = button.is_over(mouse_pos)

    # Handle events
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            return False, mouse_grid_x, mouse_grid_y
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Left click
            if event.button == 1 and not game_manager.game_over and not game_manager.animation_in_progress:

                # Check for network turn (add this block)
                if game_manager.is_networked and not game_manager.is_my_turn():
                    # Not our turn in network game, ignore input
                    continue

                # Check if an action button was clicked
                handle_button_click(action_buttons, mouse_pos, game_manager)

                # Check if grid was clicked and action was selected
                if game_manager.selected_action and (0 <= mouse_grid_x < GRID_SIZE and 0 <= mouse_grid_y < GRID_SIZE):
                    game_manager.apply_action(mouse_grid_x, mouse_grid_y)

                    # Clear button selection
                    for button in action_buttons:
                        button.selected = False

    return True, mouse_grid_x, mouse_grid_y


def handle_button_click(action_buttons, mouse_pos, game_manager):
    """
    Handles button clicks for action selection.
    """

    action_length = len(game_manager.players[0].actions)

    # Clear selection on all buttons
    for button in action_buttons:
        button.selected = False

    for i, button in enumerate(action_buttons):
        if button.is_over(mouse_pos):
            # Determine which player the button belongs to
            player_idx = i // action_length # This will be 0 if player 1 and 1 if player 2 (so clever)

            # Only allow current players button to be clicked
            if player_idx == game_manager.current_player_index:
                action_idx = i % action_length # Modulo leaves the reminder of division, but if a < b it just equals a

                # Get the action object
                action = game_manager.players[player_idx].actions[action_idx]

                # Pass the action to GameManager
                game_manager.select_action(action)
                print(f"Selected action {action.name}")
                button.selected = True


def draw_player_infos(screen, game_manager, action_buttons, font):
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

    for i, button in enumerate(action_buttons):
        button.draw(screen, button_font)


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
    if game_manager.selected_action:
        action_text = "Select starting cell"
        action_surface = font.render(action_text, True, WHITE)
        action_rect = action_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        screen.blit(action_surface, action_rect)

    # Network status (if networked)
    if game_manager.is_networked:
        if game_manager.waiting_for_remote:
            status_text = "Waiting for other player..."
            status_color = (255, 200, 100)  # Orange-yellow
        else:
            status_text = "Your turn"
            status_color = (100, 255, 100)  # Light green

        status_surface = font.render(status_text, True, status_color)
        screen.blit(status_surface, (SCREEN_WIDTH // 2 - status_surface.get_width() // 2, 75))


def show_game_over_screen(screen, game_manager, title_font, font):
    """
    Unified game over screen for both local and network games.
    Shows the winner and score, and in network mode also shows personalized win/lose message.
    """
    player1, player2 = game_manager.players

    # Determine the winner
    if player1.cells_conquered > player2.cells_conquered:
        winner = player1.name
        winner_id = 1
    elif player2.cells_conquered > player1.cells_conquered:
        winner = player2.name
        winner_id = 2
    else:
        winner = "Draw"
        winner_id = 0

    # For network games, determine if local player won or lost
    if game_manager.is_networked:
        is_player1 = game_manager.is_host  # Host is player 1

        if winner_id == 0:  # Draw
            result = "It's a Draw!"
            result_color = (255, 200, 0)  # Yellow
        elif (winner_id == 1 and is_player1) or (winner_id == 2 and not is_player1):
            result = "You Win!"
            result_color = (100, 255, 100)  # Green
        else:
            result = "You Lose!"
            result_color = (255, 100, 100)  # Red
    else:
        # For local games, show the winner but no personal result
        result = None

    # Duration before auto-exit (5 seconds) for both network and local games
    screen_duration = 5000

    # Get the scores
    player1_score = f"{player1.name}: {player1.cells_conquered} cells"
    player2_score = f"{player2.name}: {player2.cells_conquered} cells"

    # Track start time for network game countdown
    start_time = pygame.time.get_ticks()

    # Game over screen loop
    showing_game_over = True

    while showing_game_over:
        current_time = pygame.time.get_ticks()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Allow early exit on any key or click in any mode
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # Exit immediately
                if game_manager.network_manager:
                    game_manager.network_manager.disconnect()
                pygame.quit()
                sys.exit()

        # Check if time is up for auto-exit (both local and network games)
        if current_time - start_time >= screen_duration:
            # Time to exit
            showing_game_over = False

            # Clean up network resources
            if game_manager.network_manager:
                game_manager.network_manager.disconnect()

            # Exit the game completely
            pygame.quit()
            sys.exit()

        # Draw game over screen
        screen.fill(BLACK)

        # Game over title
        game_over_text = title_font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(game_over_text, game_over_rect)

        # Winner text
        winner_text = title_font.render(f"Winner: {winner}", True, WHITE)
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(winner_text, winner_rect)

        # Result text (only for network games)
        if game_manager.is_networked and result:
            result_text = title_font.render(result, True, result_color)
            result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
            screen.blit(result_text, result_rect)

        # Scores
        player1_text = font.render(player1_score, True, player1.color)
        player1_rect = player1_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(player1_text, player1_rect)

        player2_text = font.render(player2_score, True, player2.color)
        player2_rect = player2_text.get_rect(center=(SCREEN_WIDTH // 2, 340))
        screen.blit(player2_text, player2_rect)

        # Exit countdown for both local and network games
        seconds_left = (screen_duration - (current_time - start_time)) // 1000 + 1
        exit_text = font.render(f"Closing game in {seconds_left} seconds...", True, WHITE)

        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        screen.blit(exit_text, exit_rect)

        pygame.display.flip()
        pygame.time.delay(10)  # Prevent high CPU usage

    # For local games, return to allow continuing
    return


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


def draw_action_description(screen, font, game_manager, action_buttons, mouse_pos):
    """
    Draw the description of an action when hovering over its button.
    """
    action_length = len(game_manager.players[0].actions)

    for i, button in enumerate(action_buttons):
        if button.hover:
            # Determine which player's button this is
            player_idx = i // action_length
            button_idx = i % action_length

            # Get Button
            action = game_manager.players[player_idx].actions[button_idx]

            # Draw description
            description_surface = font.render(action.description, True, WHITE)
            description_rectangle = description_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
            screen.blit(description_surface, description_rectangle)
            break


def render_game(screen, game_manager, font, title_font, action_buttons, grid_x, grid_y, mouse_grid_x, mouse_grid_y):
    """
    Render the game screen.
    """
    # Fill the screen
    screen.fill(BLACK)

    # Draw each component
    draw_grid(screen, game_manager, grid_x, grid_y, mouse_grid_x, mouse_grid_y)
    draw_player_infos(screen, game_manager, action_buttons, font)
    draw_game_info(screen, game_manager, font, title_font)
    draw_action_description(screen, font, game_manager, action_buttons, mouse_pos)

    # Update the display
    pygame.display.flip()


def show_main_menu():
    """
    Show a simple main menu to choose game mode.
    """
    # Create button rectangles
    local_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 200, 200, 50)
    host_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 270, 200, 50)
    join_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 340, 200, 50)

    # Main menu loop
    menu_running = True
    while menu_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if local_button.collidepoint(mouse_pos):
                    return "local"
                elif host_button.collidepoint(mouse_pos):
                    return "host"
                elif join_button.collidepoint(mouse_pos):
                    return "join"

        # Draw menu
        screen.fill(BLACK)

        # Draw title
        title_surface = title_font.render("Cell Wars", True, WHITE)
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 100))

        # Draw buttons
        pygame.draw.rect(screen, (0, 175, 185), local_button)
        pygame.draw.rect(screen, WHITE, local_button, 2)  # White border
        local_text = font.render("Local Game", True, WHITE)
        screen.blit(local_text, (local_button.centerx - local_text.get_width() // 2,
                                 local_button.centery - local_text.get_height() // 2))

        pygame.draw.rect(screen, (0, 175, 185), host_button)
        pygame.draw.rect(screen, WHITE, host_button, 2)  # White border
        host_text = font.render("Host Game", True, WHITE)
        screen.blit(host_text, (host_button.centerx - host_text.get_width() // 2,
                                host_button.centery - host_text.get_height() // 2))

        pygame.draw.rect(screen, (0, 175, 185), join_button)
        pygame.draw.rect(screen, WHITE, join_button, 2)  # White border
        join_text = font.render("Join Game", True, WHITE)
        screen.blit(join_text, (join_button.centerx - join_text.get_width() // 2,
                                join_button.centery - join_text.get_height() // 2))

        # Update display
        pygame.display.flip()

        # Cap framerate
        pygame.time.Clock().tick(30)


def host_game_screen():
    """
    Show hosting screen and wait for connection.
    """

    # Create network host
    from network import NetworkHost
    network = NetworkHost()

    # Get local IP
    import socket
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except:
        local_ip = "Unknown"

    # Start hosting in background thread
    connected = [False]

    def start_hosting():
        connected[0] = network.host_game()

    import threading
    hosting_thread = threading.Thread(target=start_hosting, daemon=True)
    hosting_thread.start()

    # Wait for connection
    clock = pygame.time.Clock()
    dots = ""
    dot_time = 0

    while not connected[0] and hosting_thread.is_alive():
        current_time = pygame.time.get_ticks()

        # Update dots animation every 500ms
        if current_time - dot_time > 500:
            dots = "." * ((len(dots) + 1) % 4)
            dot_time = current_time

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                network.disconnect()
                pygame.quit()
                sys.exit()

        # Draw waiting screen
        screen.fill(BLACK)

        title = title_font.render("Hosting Game", True, WHITE)
        ip_text = font.render(f"Your IP: {local_ip}", True, WHITE)
        port_text = font.render(f"Port: {network.default_port}", True, WHITE)
        waiting_text = font.render(f"Waiting for player to connect{dots}", True, WHITE)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(ip_text, (SCREEN_WIDTH // 2 - ip_text.get_width() // 2, 180))
        screen.blit(port_text, (SCREEN_WIDTH // 2 - port_text.get_width() // 2, 220))
        screen.blit(waiting_text, (SCREEN_WIDTH // 2 - waiting_text.get_width() // 2, 280))

        pygame.display.flip()
        clock.tick(30)

    # Check result
    if connected[0]:
        return network
    else:
        return None


def join_game_screen():
    """
    Show joining screen and get host IP.
    """
    from network import NetworkClient

    # IP input variables
    ip_text = ""

    # Input loop
    clock = pygame.time.Clock()

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Try to connect with entered IP
                    if ip_text:
                        # Show "Connecting..." message
                        screen.fill(BLACK)
                        connecting_text = font.render(f"Connecting to {ip_text}...", True, WHITE)
                        screen.blit(connecting_text, (SCREEN_WIDTH // 2 - connecting_text.get_width() // 2, 200))
                        pygame.display.flip()

                        # Try to connect
                        network = NetworkClient()
                        if network.join_game(ip_text):
                            return network
                        else:
                            # Show error briefly
                            screen.fill(BLACK)
                            error_text = font.render("Connection failed!", True, (255, 100, 100))
                            screen.blit(error_text, (SCREEN_WIDTH // 2 - error_text.get_width() // 2, 200))
                            pygame.display.flip()
                            pygame.time.wait(2000)  # Show error for 2 seconds
                            ip_text = ""  # Clear for retry
                elif event.key == pygame.K_BACKSPACE:
                    ip_text = ip_text[:-1]
                elif event.unicode in "0123456789.":
                    # Only allow numbers and periods for IP address
                    if len(ip_text) < 15:  # Reasonable length limit
                        ip_text += event.unicode

        # Draw IP input screen
        screen.fill(BLACK)

        title = title_font.render("Join Game", True, WHITE)
        prompt = font.render("Enter Host IP Address:", True, WHITE)
        current_ip = font.render(ip_text, True, WHITE)
        hint = font.render("(Press Enter when done)", True, WHITE)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 180))

        # IP input box
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, 220, 200, 40)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        screen.blit(current_ip, (input_box.x + 10, input_box.y + 10))

        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 280))

        pygame.display.flip()
        clock.tick(30)


def handle_network_disconnection(screen, game_manager, font, title_font):
    """
    Shows a disconnection message and exits the game after a delay.
    """
    # Clean up network resources
    if game_manager.network_manager:
        game_manager.network_manager.disconnect()

    # Display message duration
    DISCONNECT_MESSAGE_DURATION = 3000  # 3 seconds
    start_time = pygame.time.get_ticks()

    # Display disconnection message until duration expires
    while pygame.time.get_ticks() - start_time < DISCONNECT_MESSAGE_DURATION:
        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw disconnection message
        screen.fill(BLACK)

        # Main disconnect message
        disconnect_text = title_font.render("Connection Lost!", True, (255, 50, 50))
        text_rect = disconnect_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))

        # Background for text
        bg_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)
        pygame.draw.rect(screen, (255, 50, 50), bg_rect, 2)

        screen.blit(disconnect_text, text_rect)

        # Exiting message
        exit_text = font.render("Exiting game...", True, WHITE)
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(exit_text, exit_rect)

        pygame.display.flip()
        pygame.time.delay(10)  # Prevent high CPU usage

    # Exit game
    pygame.quit()
    sys.exit()

# ==================== GAME MENU & NETWORK MODE ==================== #

# == Show main menu first
game_mode = show_main_menu()

# Initialize network manager based on mode
network_manager = None
if game_mode == "host":
    network_manager = host_game_screen()
    if not network_manager:  # If hosting failed
        pygame.quit()
        sys.exit()
elif game_mode == "join":
    network_manager = join_game_screen()
    if not network_manager:  # If joining failed
        pygame.quit()
        sys.exit()


# ==================== GAME SETUP ==================== #

# == Create the game manager
game_manager = GameManager(GRID_SIZE, GRID_SIZE, CELL_SIZE, network_manager)
game_manager.initialize_players("Player 1", "Player 2")
if game_manager.is_networked:
    game_manager.waiting_for_remote = not game_manager.is_my_turn()

# == Create action buttons
action_buttons = []

# ==== Player 1 buttons (left side)
for i, action in enumerate(game_manager.players[0].actions):
    button_rect = pygame.Rect(50, 250 + i * 50, 130, 40)
    action_buttons.append(Button(button_rect, action.name, game_manager.players[0].color))

# ==== Player 2 buttons (right side)
for i, action in enumerate(game_manager.players[1].actions):
    button_rect = pygame.Rect(SCREEN_WIDTH - 180, 250 + i * 50,130,40)
    action_buttons.append(Button(button_rect, action.name, game_manager.players[1].color))

# == Calculate grid coordinates
grid_surface_width = GRID_SIZE * CELL_SIZE
grid_surface_height = GRID_SIZE * CELL_SIZE
grid_x = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
grid_y = (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) // 2


# ==================== GAME LOOP ==================== #

running = True
mouse_grid_x, mouse_grid_y = 0,0

while running:
    # == Get current time for animation timing
    current_time = pygame.time.get_ticks()

    # == Handle network disconnection
    if game_manager.is_networked and not game_manager.check_network_connection():
        print("Network disconnection detected!")
        handle_network_disconnection(screen, game_manager, font, title_font)

     # == Check for game over
    if game_manager.game_over:
        show_game_over_screen(screen, game_manager, title_font, font)


    # == Get Mouse position
    mouse_pos = pygame.mouse.get_pos()

    # == Handle input
    running, mouse_grid_x, mouse_grid_y = handle_input(mouse_pos, grid_x, grid_y, game_manager, action_buttons)

    # Update game state (for animation and networking)
    game_manager.update(current_time)

    # == Render game
    render_game(screen, game_manager, font, title_font, action_buttons, grid_x, grid_y, mouse_grid_x, mouse_grid_y)

# == Network cleanup
if network_manager:
    network_manager.disconnect()

# == Quit the game
pygame.quit()
sys.exit()









