import pygame, time
import random

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


class SnakePattern(CellularAutomaton):
    """
    A cellular automaton that creates a winding snake-like pattern.
    This pattern grows in a continuous path that can turn and change direction,
    creating a snake-like pattern across the grid.

    Subclass of CellularAutomaton.
    """

    def __init__(self, grid, player_id, generations=10, overwrite_neutral=True, overwrite_enemy=False):
        super().__init__(grid, player_id, generations, overwrite_neutral, overwrite_enemy) #This inits the inherited function
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
        self.snake_segments = []  # To keep track of the snake's path
        self.current_direction = None

    def set_starting_cell(self, x, y):
        """
        Override to initialize the snake's starting position and direction
        """
        if 0 <= x < self.grid.width and 0 <= y < self.grid.height:
            self.possible_cells = set([(x, y)])
            self.snake_segments = [(x, y)]
            self.current_direction = random.choice(self.directions)  # Start in a random direction
            return [[x, y, self.player_id]]
        return []

    def simulate_step(self, current_x, current_y, temp_grid, can_conquer_func, next_gen_cells):
        """
        Simulate one step of the snake pattern.
        The snake tries to continue moving in its current direction,
        but will change direction if blocked.
        """
        changes = []

        # If we have a current direction, try to continue in that direction
        if self.current_direction:
            # Try the current direction first
            direction_options = [self.current_direction]

            # Add all other directions (in case we need to turn)
            for direction in self.directions:
                if direction != self.current_direction:
                    direction_options.append(direction)

            # Try each direction until we find a valid one
            moved = False
            for dx, dy in direction_options:
                new_x, new_y = current_x + dx, current_y + dy

                # Check if we can move to this cell
                if can_conquer_func(new_x, new_y):
                    # Update the temp grid
                    temp_grid[new_y][new_x] = self.player_id

                    # Add this cell to our next generation
                    next_gen_cells.add((new_x, new_y))

                    # Record the change
                    changes.append([new_x, new_y, self.player_id])

                    # Update the snake's path
                    self.snake_segments.append((new_x, new_y))

                    # Update our current direction
                    self.current_direction = (dx, dy)

                    moved = True
                    break

            # If we couldn't move in any direction, we're stuck
            if not moved:
                # Try a random cell from our path as a new head
                if len(self.snake_segments) > 1:
                    # Skip the last segment (current head) and try from somewhere else
                    for i in range(len(self.snake_segments) - 2, -1, -1):
                        x, y = self.snake_segments[i]
                        # Try each direction from this segment
                        for dx, dy in self.directions:
                            new_x, new_y = x + dx, y + dy
                            if can_conquer_func(new_x, new_y):
                                # Start a new branch
                                temp_grid[new_y][new_x] = self.player_id
                                next_gen_cells.add((new_x, new_y))
                                changes.append([new_x, new_y, self.player_id])
                                self.snake_segments.append((new_x, new_y))
                                self.current_direction = (dx, dy)
                                moved = True
                                break
                        if moved:
                            break

        return changes


class RootGrowth(CellularAutomaton):
    """
    A cellular automaton that mimics how tree roots grow and branch out.
    This pattern creates a natural-looking root system with rapidly decreasing
    probability of growth for each direction checked and each generation.

    Subclass of CellularAutomaton.
    """

    def __init__(self, grid, player_id, generations=7, overwrite_neutral=True, overwrite_enemy=False):
        # Call the parent class constructor to set up basic properties
        super().__init__(grid, player_id, generations, overwrite_neutral, overwrite_enemy)

        # The initial conquest probability for the first cell (90% chance)
        self.initial_probability = 0.9

        # How much to reduce probability for each new direction checked
        self.probability_decrease = 0.3

        # How much to reduce the starting probability for each new generation of cells
        self.generation_decrease = 0.25

        # Maximum generation - roots stop growing after this many steps
        self.max_generations = generations

        # Dictionary to track each cell's generation number
        self.cell_generations = {}

    def set_starting_cell(self, x, y):
        """Override to initialize the root's starting position and generation tracking"""
        if 0 <= x < self.grid.width and 0 <= y < self.grid.height:
            self.possible_cells = set([(x, y)])
            self.cell_generations[(x, y)] = 0  # Starting cell is generation 0
            return [[x, y, self.player_id]]
        return []

    def simulate_step(self, current_x, current_y, temp_grid, can_conquer_func, next_gen_cells):
        """
        Simulate one step of the root growth pattern for a specific cell.

        Args:
            current_x, current_y: The coordinates of the current cell
            temp_grid: Temporary grid for simulation
            can_conquer_func: Function to check if a cell can be conquered
            next_gen_cells: Set to store cells for the next generation

        Returns:
            List of changes made during this step
        """
        # This list will store all changes we make
        changes = []

        # Get this cell's generation number
        current_generation = self.cell_generations.get((current_x, current_y), 0)

        # If we've reached the maximum generation, stop growing from this cell
        if current_generation >= self.max_generations - 1:
            return []

        # Calculate the starting probability for this cell
        # Each successive generation has a lower starting probability
        start_probability = max(0.1, self.initial_probability - (current_generation * self.generation_decrease))

        # Define all eight possible directions we can grow in (orthogonal and diagonal)
        # The eight directions are: Up, Up-Right, Right, Down-Right, Down, Down-Left, Left, Up-Left
        all_directions = [
            (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)
        ]

        # Shuffle the directions to randomize which one we try first
        # This creates more natural, unpredictable growth patterns
        random.shuffle(all_directions)

        # Keep track of our current conquest probability
        current_probability = start_probability

        # Try each direction with decreasing probability
        for dx, dy in all_directions:
            # Calculate the new coordinates
            new_x = current_x + dx
            new_y = current_y + dy

            # Check if we can grow to this cell (is it empty or can we take it over?)
            if can_conquer_func(new_x, new_y):
                # Roll a random number to see if we conquer this cell
                if random.random() < current_probability:
                    # Success! Mark this cell as belonging to our player
                    temp_grid[new_y][new_x] = self.player_id

                    # Add this cell to the next generation set
                    # This means this cell will be active in the next step
                    next_gen_cells.add((new_x, new_y))

                    # Record the change for animation
                    changes.append([new_x, new_y, self.player_id])

                    # Mark this new cell as being one generation higher than its parent
                    self.cell_generations[(new_x, new_y)] = current_generation + 1

                # Decrease the probability for the next direction we check
                # This makes it less likely to grow in multiple directions
                current_probability = max(0.05, current_probability - self.probability_decrease)

        # Return all the changes we made during this step
        return changes