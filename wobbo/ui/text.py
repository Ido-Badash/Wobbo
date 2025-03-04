import pygame

class Text:
    """A class for displaying pygame text on a surface."""
    def __init__(self, text: str, font: pygame.font.Font, color: tuple[int, int, int], alpha: int = 255,
                 antialias: bool = True, bg_color: tuple[int, int, int] = None):
        self.text = text
        self.font = font
        self.color = color
        self.alpha = alpha
        self.antialias = antialias
        self.bg_color = bg_color
        self.text_surf = self.font.render(self.text, self.antialias, self.color, self.bg_color)
        
    def update(self):
        self.text_surf = self.font.render(self.text, self.antialias, self.color, self.bg_color)
        self.text_surf.set_alpha(self.alpha)
        
    def render(self, surface: pygame.Surface, x: int, y: int):
        """Draws the text on the surface at the given position."""
        surface.blit(self.text_surf, (x, y))
        
    def fade_out(self, timer: int, fade_after: int = 0, fade_speed: int = 1, min_alpha: int = 0, start_fade: bool = True):
        """Fades out the text by reducing the alpha value. Returns True when fade is finished.
        The `fade_after` parameter is the time in milliseconds before fading starts."""
        if start_fade:
            if timer > fade_after:
                self.alpha -= fade_speed
                if self.alpha <= min_alpha:
                    self.alpha = min_alpha
                    start_fade = False
                    return True
        return False
        
    def get_rect(self) -> pygame.Rect:
        """Returns the rectangle of the text surface."""
        return self.text_surf.get_rect()
    
    def set_font(self, font: pygame.font.Font):
        """Sets the font."""
        self.font = font
        self.update()
    
    def set_text(self, text: str):
        """Sets the text."""
        self.text = text
        self.update()
    
def render_fade_out_text(surf: pygame.Surface, reset_timer: int,
                        text: Text, text_pos: tuple[int, int],
                        fade_after: int = 0, fade_speed: int = 1,
                        min_alpha: int = 0, start_fade: bool = True):
    text_fade_timer = pygame.time.get_ticks() - reset_timer
    text.fade_out(
        timer=text_fade_timer,
        fade_after=fade_after,
        fade_speed=fade_speed,
        min_alpha=min_alpha,
        start_fade=start_fade
        
    )
    text.render(surf,
        text_pos[0],
        text_pos[1])