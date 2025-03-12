import pygame
from cellular_automaton import SimpleExpansion
from player import Player
from grid import Grid
from player_action import PlayerAction
from cellular_automaton import CellularAutomaton


class GameManager:
    def __init__(self, grid_width, grid_height, cell_size, network_manager = None):
        self.grid = Grid(grid_width, grid_height, cell_size) #Initializes the grid
        self.players = []
        self.current_player_index = 0
        self.selected_action = None # Stores the selected action as object
        self.total_turns = 10
        self.current_turn = 1
        self.game_over = False

        # Animation properties
        self.animation_in_progress = False
        self.animation_changes = None # List of all changes to animate (format: [[x1,y1,player_id], [x2,y2,player_id], ...])
        self.animation_index = 0
        self.step_delay = 50  # milliseconds between animation steps
        self.next_step_time = 0
        self.changes_per_step = 1  # Number of cells to update per animation step

        # Network properties
        self.network_manager = network_manager
        self.is_host = network_manager is not None and network_manager.__class__.__name__ == 'NetworkHost'
        self.is_client = network_manager is not None and network_manager.__class__.__name__ == 'NetworkClient'
        self.is_networked = network_manager is not None
        self.waiting_for_remote = False # True when waiting for the other player to take their turn

    def initialize_players(self, player1_name, player2_name):
        """
        Create the two Players.
        """
        #Colors
        player1_color = (0, 175, 185)  # Verdigris
        player2_color = (240, 113, 103)  # Bittersweet

        player1 = Player(1, player1_name, player1_color)
        player2 = Player(2, player2_name, player2_color)

        """
        Player action.
        Creates the actions each player can chose.
        Name, description, CA to use, number of generations, if can overwrite neutral tiles, if can overwrite enemy tiles, price
        """
        simple_expansion = PlayerAction(
            "Diamond Bomb",
            "Expands in a diamond shape",
            SimpleExpansion,
            generations = 3
        )

        snake_pattern = PlayerAction(
            "Snake Attack",
            "Slithers like a snake",
            SimpleExpansion, # Change Later
            generations = 10
        )

        root_growth = PlayerAction(
            "Root Growth",
            "Spread like a tree root",
            SimpleExpansion, # Change Later
            generations = 7
        )

        # Add actions to players
        player1.add_action(simple_expansion)
        player1.add_action(simple_expansion)
        player1.add_action(simple_expansion)

        player2.add_action(simple_expansion)
        player2.add_action(simple_expansion)
        player2.add_action(simple_expansion)

        self.players = [player1, player2]

        #Update grid with player colors
        self.grid.update_player_colors(player1_color, player2_color)

    def get_current_player(self):
        """
        Get the player whose turn it is.
        """

        return self.players[self.current_player_index]

    def next_turn(self):
        """
        Switch to next players turn.
        """

        # Count players cells
        self.update_cell_count()

        #Switch Player
        self.current_player_index = 1 - self.current_player_index  # Toggle between 0 and 1

        # Increment turn counter if back to first player
        if self.current_player_index == 0:
            self.current_turn += 1

        # Check if game is over
        if self.current_turn > self.total_turns:
            self.game_over = True

        # In networked games, check if it's our turn
        if self.is_networked:
            self.waiting_for_remote = not self.is_my_turn()

    def select_action(self, action):
        """
        The action that the player has selected.
        """
        
        self.selected_action = action


    def apply_action(self, grid_x, grid_y):
        """
        Apply the selected action at the given coordinates.
        - Verifies that an action is selected, the game isn't over, and no animation is in progress
        - Creates the automaton from the selected action and sets the starting cell
        - Runs the automaton and captures all changes
        - In networked mode, sends these changes to the other player
        - Starts animation playback in all cases
        """
        # Check if we can apply the action
        if not self.selected_action or self.game_over or self.animation_in_progress:
            return False

        # Check if it's our turn in networked mode
        if self.is_networked and not self.is_my_turn():
            return False

        current_player = self.get_current_player()

        # Create the automaton
        automaton = self.selected_action.create_automaton(self.grid, current_player.player_id)

        # Set starting cell and get initial grid changes
        initial_grid_changes = automaton.set_starting_cell(grid_x, grid_y)

        # Run and capture all changes
        all_changes = initial_grid_changes + automaton.run()

        # If in networked mode, send to other player
        if self.is_networked:
            message = {
                "type": "action_result",
                "action_name": self.selected_action.name,
                "grid_x": grid_x,
                "grid_y": grid_y,
                "changes": all_changes
            }
            self.network_manager.send_message(message)

        # Start animated playback (for both local and networked games)
        self.start_animation_playback(all_changes)

        return True

    def update_cell_count(self):
        """
        Count and update the number of cells owned by each player.
        """

        counts = {1: 0, 2: 0}

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell_state = self.grid.get_cell(x, y)
                if cell_state in counts:
                    counts[cell_state] += 1

        for player in self.players:
            player.update_cells_conquered(counts.get(player.player_id, 0))

    def start_animation_playback(self, changes):
        """
        Start animation playback.
        - Takes a list of cell changes to animate.
        - Sets up the animation state (resets index, marks animation as in progress).
        - Schedules the first animation step.
        - Clears the selected action.
        """

        # Store changes for animation
        self.animation_changes = changes
        self.animation_index = 0
        self.animation_in_progress = True
        self.next_step_time = pygame.time.get_ticks() + self.step_delay

        # Clear selected action
        self.selected_action = None

    def update_animation(self, current_time):
        """
        Update animation state
        - Checks if it's time for the next animation step
        - Applies a batch of changes (controlled by changes_per_step)
        - Updates the animation index
        - Schedules the next batch
        - Ends the animation and calls next_turn() when all changes are applied
        """

        if not self.animation_in_progress or not self.animation_changes:
            return

        if current_time >= self.next_step_time:
            # Apply next batch of changes
            changes_applied = 0

            while changes_applied < self.changes_per_step and self.animation_index < len(self.animation_changes):
                # Get the next change
                change = self.animation_changes[self.animation_index]
                x, y, player_id = change

                # Apply the change
                self.grid.set_cell(x, y, player_id)

                # Update counters
                self.animation_index += 1
                changes_applied += 1

            # Schedule next batch
            self.next_step_time = current_time + self.step_delay

            # Check if animation is complete
            if self.animation_index >= len(self.animation_changes):
                # Animation complete
                self.animation_in_progress = False
                self.animation_changes = None

                # Move to next turn
                self.next_turn()

    def is_my_turn(self):
        """
        Check if it's this client's turn in a networked game.
        """

        if not self.is_networked:
            return True  # Always our turn in local game

        return (
                (self.is_host and self.current_player_index == 0) or
                (self.is_client and self.current_player_index == 1)
        )

    def process_network_messages(self):
        """
        Process any pending network messages.
        - Checks if there are any new messages from the network_manager.
        - Handles "action_result" messages by extracting the changes.
        - Starts the animation playback with those changes.
        """

        if not self.is_networked or not self.network_manager:
            return

        message = self.network_manager.get_next_message()

        if not message:
            return

        if message.get("type") == "action_result" and "changes" in message:
            # Extract data
            changes = message["changes"]
            # Start animated playback
            self.start_animation_playback(changes)
        else:
            print(f"Received unknown message type: {message}")

    def update (self, current_time):
        """
        Update game state - call this every frame.
        - Acts as the main update method called every frame
        - First checks for network messages
        - Then updates any ongoing animation
        """

        # Check for network messages
        self.process_network_messages()

        # Update animation
        self.update_animation(current_time)