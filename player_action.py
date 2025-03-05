class PlayerAction:
    """
    An action that a player can choose.
    Each action is associated with a specific cellular automaton.
    """

    def __init__(self, name, description, automaton_class, generations=5,
                 overwrite_neutral=True, overwrite_enemy=False, cost=1):
        """
        Initialize an action.

        Args:
            name: The name of the action
            description: A brief description of what the action does
            automaton_class: The cellular automaton class to use
            generations: Number of steps the automaton will run
            overwrite_neutral: Whether this action can take over neutral cells
            overwrite_enemy: Whether this action can take over enemy cells
            cost: The cost of using this action (for future balancing)
        """

        self.name = name
        self.description = description
        self.automaton_class = automaton_class
        self.generations = generations
        self.overwrite_neutral = overwrite_neutral
        self.overwrite_enemy = overwrite_enemy
        self.cost = cost

    def create_automaton(self, grid, player_id):
        """
        Create an instance of this action's automaton.
        """

        return self.automaton_class(grid,
                                     player_id,
                                    generations = self.generations,
                                    overwrite_neutral = self.overwrite_neutral,
                                    overwrite_enemy = self.overwrite_enemy)