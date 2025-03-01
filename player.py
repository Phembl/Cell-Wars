class Player:
    def __init__(self, player_id, name, color):
        self.player_id = player_id
        self.name = name
        self.color = color
        self.cells_conquered = 0
        self.moves = [] # Will be used later

    def add_move(self, move):
        """Add a move to the player's moveset"""
        self.moves.append(move)

    def update_cells_conquered(self, count):
        """Update the number of cells conquered by this player"""
        self.cells_conquered = count

    def get_move_by_name(self, name):
        """Return the move with the given name"""
        for move in self.moves:
            if move.name == name:
                return move
        return None