class Player:
    def __init__(self, player_id, name, color):
        self.player_id = player_id
        self.name = name
        self.color = color
        self.cells_conquered = 0
        self.actions = []

    def add_action(self, action):
        """
        Add an action to the player's action-set.
        """

        self.actions.append(action)

    def update_cells_conquered(self, count):
        """
        Update the number of cells conquered by this player.
        """

        self.cells_conquered = count
