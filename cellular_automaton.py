import pygame, time

class CellularAutomaton:
    """
    Base class for all cellular automaton patterns.
    """
    def __init__(self, grid, player_id, generations=5, overwrite_neutral=True, overwrite_enemy=False):
        """
        Initialize the cellular automaton.

        Args:
            grid: The game grid
            player_id: ID of the player using this automaton
            generations: Number of evolution steps to perform
            overwrite_neutral: Whether this pattern can take over neutral cells
            overwrite_enemy: Whether this pattern can take over enemy cells

        Default values are defined as fallback inheritance values.

        """

        self.grid = grid
        self.player_id = player_id
        self.generations = generations
        self.overwrite_neutral = overwrite_neutral
        self.overwrite_enemy = overwrite_enemy
        self.possible_cells = set()  # Cells that are currently being processed
        self.current_generation = 0

    def set_starting_cell(self, x, y):
        """
        Set the starting cell coordinate.
        Returns the initial cell change without modifying the grid.
        """
        if 0 <= x < self.grid.width and 0 <= y < self.grid.height:
            # Add starting cell to possible_cells
            self.possible_cells.add((x, y))
            # Return the change without applying it
            return [[x, y, self.player_id]]
        return []

    def can_conquer_cell(self, x, y):
        """
        Check if a cell can be conquered based on the automaton's rules.
        """
        # Check if coordinates are within grid bounds
        if not (0 <= x < self.grid.width and 0 <= y < self.grid.height):
            return False

        cell_state = self.grid.get_cell(x,y)

        # Returns a bool based on the cells state and the overwrite settings
        # Neutral cell
        if cell_state == self.grid.NEUTRAL:
            return self.overwrite_neutral

        # Enemy cell
        if cell_state != self.player_id:
            return self.overwrite_enemy

        # Own cell (can't be conquered)
        return False

    def step(self):
        """
        Perform one step of the automaton's evolution.
        This method must be overridden by subclasses.
        """
        pass

    def run(self):
        """
        Run the automaton for the specified number of generations.
        Simulates and collects changes without applying them to the grid.
        """
        # Create a temporary grid for simulation
        temp_grid = []
        for y in range(self.grid.height):
            row = []
            for x in range(self.grid.width):
                row.append(self.grid.get_cell(x, y))
            temp_grid.append(row)

        # Set the initial cell in our temp grid
        for x, y in self.possible_cells:
            temp_grid[y][x] = self.player_id

        # Store all changes
        all_changes = []

        # Implement a temporary can_conquer method for the temp grid
        def temp_can_conquer(x, y):
            if not (0 <= x < self.grid.width and 0 <= y < self.grid.height):
                return False

            cell_state = temp_grid[y][x]

            # Neutral cell
            if cell_state == self.grid.NEUTRAL:
                return self.overwrite_neutral

            # Enemy cell
            if cell_state != self.player_id:
                return self.overwrite_enemy

            # Own cell (can't be conquered)
            return False

        # Run for specified generations
        for _ in range(self.generations):
            # If no possible cells remain, stop early
            if not self.possible_cells:
                break

            # Create temp storage for this generation's changes
            next_gen_cells = set()
            generation_changes = []

            # Let the subclass simulate one step using the temp grid
            for current_x, current_y in self.possible_cells:
                # Here we'll need to call a method that handles the specific pattern
                # but works on the temp grid instead of the real one
                changes = self.simulate_step(current_x, current_y, temp_grid, temp_can_conquer, next_gen_cells)
                generation_changes.extend(changes)

            # Update our possible cells for next generation
            self.possible_cells = next_gen_cells

            # Add this generation's changes to our full list
            all_changes.extend(generation_changes)

        return all_changes

class SimpleExpansion(CellularAutomaton):
    """
    A simple cellular automaton that expands to adjacent cells.
    This pattern grows outward from each possible cell, conquering neighboring cells
    in all four directions (up, down, left, right). It creates a diamond-shaped
    expansion pattern.

    Subclass of CellularAutomaton.
     """

    def simulate_step(self, current_x, current_y, temp_grid, can_conquer_func, next_gen_cells):
        """
        Simulate one step of the simple expansion automaton for a specific cell.
        """
        changes = []

        # Check cell above
        if can_conquer_func(current_x, current_y - 1):
            temp_grid[current_y - 1][current_x] = self.player_id
            next_gen_cells.add((current_x, current_y - 1))
            changes.append([current_x, current_y - 1, self.player_id])

        # Check cell below
        if can_conquer_func(current_x, current_y + 1):
            temp_grid[current_y + 1][current_x] = self.player_id
            next_gen_cells.add((current_x, current_y + 1))
            changes.append([current_x, current_y + 1, self.player_id])

        # Check cell left
        if can_conquer_func(current_x - 1, current_y):
            temp_grid[current_y][current_x - 1] = self.player_id
            next_gen_cells.add((current_x - 1, current_y))
            changes.append([current_x - 1, current_y, self.player_id])

        # Check cell right
        if can_conquer_func(current_x + 1, current_y):
            temp_grid[current_y][current_x + 1] = self.player_id
            next_gen_cells.add((current_x + 1, current_y))
            changes.append([current_x + 1, current_y, self.player_id])

        return changes