import pygame

WHITE = (240, 246, 239)

#-- Button Class
class Button:
    """
    Create a button with a given rectangle, text and color.

           Arguments:
            rect (pygame.Rect): Position and size of button
            text (str): Text to display on button
            color (tuple): RGB color tuple for the button
    """
    def __init__(self, rect, text, color):
        self.rect = rect
        self.text = text
        self.color = color
        self.hover = False
        self.selected = False

    def draw(self, surface, font):
        """
        Draw the button on the given surface.

        Args:
            surface: Pygame surface to draw on
            font: Pygame font to use for text
        """
        # Draw Button BG
        if self.hover:
            # Brighten color when hovered
            hover_color = (min(self.color[0] + 50,255),
                           min(self.color[1] + 50, 255),
                           min(self.color[2] + 50, 255))
            pygame.draw.rect(surface, hover_color, self.rect)

        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # Draw Button Border
        #pygame.draw.rect(surface, (240, 246, 239), self.rect, 2) #Border

        # Draw Button highlight if selected
        if self.selected:
            pygame.draw.rect(surface, WHITE, self.rect.inflate(10, 10), 3)

        # Draw Button text
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_over(self, pos):
        """
         Check if the given position is over this button.

         Args:
             pos (tuple): (x, y) position to check

         Returns:
             bool: True if position is over button, False otherwise
         """
        return self.rect.collidepoint(pos)



