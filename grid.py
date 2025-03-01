import pygame

class Grid:
    # Cell states
    NEUTRAL = 0
    PLAYER1 = 1
    PLAYER2 = 2

    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = [[self.NEUTRAL for x in range(width)] for y in range(height)]

        # Colors
        self.colors = {
            self.NEUTRAL: (100,100,100), # Gray
            self.PLAYER1: (255,150,150), # Pink
            self.PLAYER2: (255,200,150) # Yellow
        }

    def set_cell(self, x, y, state):
        """ Set the state of a cell at a given coordinate."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x] = state

    def get_cell(self, x, y):
        """Get the state of a cell at the given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None

    def draw(self, surface, linecolor):
        """Draw the grid on the given surface."""
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(surface, self.colors[self.cells[y][x]], rect)
                pygame.draw.rect(surface, linecolor, rect, 1)  # Grid lines