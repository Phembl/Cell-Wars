from cellular_automaton import SimpleExpansion
from player import Player
from grid import Grid
from player_action import PlayerAction
from cellular_automaton import CellularAutomaton


class GameManager:
    def __init__(self, grid_width, grid_height, cell_size):
        self.grid = Grid(grid_width, grid_height, cell_size) #Initializes the grid
        self.players = []
        self.current_player_index = 0
        self.selected_action = None # Stores the selected action as object
        self.total_turns = 10
        self.current_turn = 1
        self.game_over = False

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
        Name, description, CA to use, number of generations, can overwrite neutral tiles, can overwrite enemy tiles, price
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

    def select_action(self, action):
        """
        The action that the player has selected.
        """
        
        self.selected_action = action

    #Needs to be discussed further:
    def apply_action(self, grid_x, grid_y):
        """
        Apply the selected action at the given coordinates.
        """

        if self.selected_action and not self.game_over:
            current_player = self.get_current_player()

            # Create and run the automaton
            automaton = self.selected_action.create_automaton(self.grid, current_player.player_id)
            automaton.set_starting_cell(grid_x, grid_y)
            automaton.run()

            # Clear selected action
            self.selected_action = None

            # Next turn
            self.next_turn()

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