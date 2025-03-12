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
        """
        if 0 <= x < self.grid.width and 0 <= y < self.grid.height: # Defensive programming, avoids error if non-existing coordinate is given
            # Set the cell to the player's color
            self.grid.set_cell(x, y, self.player_id)
            self.possible_cells.add((x, y))

            #Return the starting cell
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
        """
        for _ in range(self.generations): # Usage of _ because counter is never used and doesn't require variable (pure convention)
            # If no possible cells remain, stop early
            if not self.possible_cells:
                break

            # Perform one step
            self.step()

            # Add a delay to see the growth
            pygame.display.flip()  # Update the display to show changes
            pygame.time.delay(200)  # Delay for 100 milliseconds

        # Return the total number of cells conquered
        return self.count_player_cells()

    def count_player_cells(self):
        """
        Counts the number of cells owned by the player.
        """
        count = 0
        for y in range(0, self.grid.height):
            for x in range(0, self.grid.width):
                if self.grid.get_cell(x, y) == self.player_id:
                    count += 1
        return count

class SimpleExpansion(CellularAutomaton):
    """
    A simple cellular automaton that expands to adjacent cells.
    This pattern grows outward from each possible cell, conquering neighboring cells
    in all four directions (up, down, left, right). It creates a diamond-shaped
    expansion pattern.

    Subclass of CellularAutomaton.
     """

    def step(self):
        # Create an empty set to store the new possible cells for the next generation
        next_generation_cells = set()
        changes = [] # Tracks changes for networking

        for current_x, current_y in self.possible_cells:
            # For each current cell, check all four neighboring directions

            # Check cell above
            if self.can_conquer_cell(current_x, current_y - 1):
                self.grid.set_cell(current_x, current_y - 1, self.player_id)
                next_generation_cells.add((current_x, current_y - 1))
                changes.append([current_x, current_y - 1, self.player_id])

            # Check cell below
            if self.can_conquer_cell(current_x, current_y + 1):
                self.grid.set_cell(current_x, current_y + 1, self.player_id)
                next_generation_cells.add((current_x, current_y + 1))
                changes.append([current_x, current_y + 1, self.player_id])

            # Check cell left
            if self.can_conquer_cell(current_x - 1, current_y):
                self.grid.set_cell(current_x - 1, current_y, self.player_id)
                next_generation_cells.add((current_x - 1, current_y))
                changes.append([current_x - 1, current_y, self.player_id])

            # Check cell right
            if self.can_conquer_cell(current_x + 1, current_y):
                self.grid.set_cell(current_x + 1, current_y, self.player_id)
                next_generation_cells.add((current_x + 1, current_y))
                changes.append([current_x + 1, current_y, self.player_id])

        # After processing all current cells, update our possible_cells for the next step
        self.possible_cells = next_generation_cells

        # Return the changes for networking
        return changes