from player import Player
from grid import Grid

class GameManager:
    def __init__(self, grid_width, grid_height, cell_size):
        self.grid = Grid(grid_width, grid_height, cell_size) #Initializes the grid
        self.players = []
        self.current_player_index = 0
        self.selected_move = None
        self.total_turns = 10
        self.current_turn = 1
        self.game_over = False

    def initialize_players(self, player1_name, player2_name):
        """Create the two Players"""
        #Colors
        player1_color = (0, 175, 185)  # Verdigris
        player2_color = (240, 113, 103)  # Bittersweet

        player1 = Player(1, player1_name, player1_color)
        player2 = Player(2, player2_name, player2_color)

        self.players = [player1, player2]

        #Update grid with player colors
        self.grid.update_player_colors(player1_color, player2_color)

    def get_current_player(self):
        """Get the player whose turn it is."""
        return self.players[self.current_player_index]

    def next_turn(self):
        """Switch to next players turn."""
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

    def select_move(self, move):
        """The move that the player has selected."""
        self.selected_move = move

    #Needs to be discussed further:
    def apply_move(self, grid_x, grid_y):
        """Apply the selected move at the given coordinates."""
        if self.selected_move and not self.game_over:
            # This is a placeholder - moves will be implemented later
            player_id = self.get_current_player().player_id
            self.grid.set_cell(grid_x, grid_y, player_id)

            # Clear selected move
            self.selected_move = None

            # Next turn
            self.next_turn()

    def update_cell_count(self):
        """Count and update the number of cells owned by each player."""
        counts = {1: 0, 2: 0}

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell_state = self.grid.get_cell(x, y)
                if cell_state in counts:
                    counts[cell_state] += 1

        for player in self.players:
            player.update_cells_conquered(counts.get(player.player_id, 0))