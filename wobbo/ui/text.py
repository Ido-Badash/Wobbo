import pygame

class Text:
    """A class for displaying pygame text on a surface."""
    def __init__(self, text: str, font: pygame.font.Font, color: tuple,
                 antialias: bool = True, bg_color: tuple = None):
        self.text = text
        self.font = font
        self.color = color
        self.antialias = antialias
        self.bg_color = bg_color
        self.text_surf = self.font.render(self.text, self.antialias, self.color, self.bg_color)
        
    def draw(self, surface: pygame.Surface, x: int, y: int):
        """Draws the text on the surface at the given position."""
        surface.blit(self.text_surf, (x, y))
                
    def set_text(self, text: str):
        self.text = text
        self.text_surf = self.font.render(self.text, self.antialias, self.color, self.bg_color)
        
    def set_color(self, color: tuple):
        self.color = color
        self.text_surf = self.font.render(self.text, self.antialias, self.color, self.bg_color)
        
    def set_bg_color(self, bg_color: tuple):
        self.bg_color = bg_color
        self.text_surf = self.font.render(self.text, self.antialias, self.color, self.bg_color)
        
    def set_font(self, font: pygame.font.Font):
        self.font = font
        self.text_surf = self.font.render(self.text, self.antialias, self.color, self.bg_color)
        
    def set_antialias(self, antialias: bool):
        self.antialias = antialias
        self.text_surf = self.font.render(self.text, self.antialias, self.color, self.bg_color)
        
        