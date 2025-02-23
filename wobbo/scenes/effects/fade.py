import pygame
import logging
from ...core.scene import Scene
from ...utils.colors import *

class Fade(Scene):
    def __init__(self, surface: pygame.Surface,
                 fade_speed: int = 1,
                 fade_color: tuple[int, int, int] = BLACK,
                 fade_type: str = "both",
                 start_fade: int = 0,
                 max_alpha: int = 255):
        """A fade effect that can be used to fade in, fade out, or both.
        Ensure `fade_type` is one of 'in', 'out', or 'both'."""
        super().__init__([])
        self.surface = surface
        self.fade_speed = fade_speed
        self.fade_color = fade_color
        self.fade_type = fade_type
        self.current_alpha = start_fade
        self.max_alpha = max_alpha
        
        self.fade_surface = pygame.Surface(self.surface.get_size())
        self.fade_surface.fill(self.fade_color)
        self.fade_surface.set_alpha(self.current_alpha)
        self.reached_middle = False
        self.run_once = False
        
        if self.fade_type not in ["in", "out", "both"]:
            raise ValueError("fade_type must be 'in', 'out', or 'both'")
        self.fade_surface.set_alpha(self.current_alpha)
          
    def handle_event(self, event: pygame.event.Event):
        pass
    
    def update(self):
        """Updates the width and height of the fade surface."""
        self.fade_surface = pygame.Surface(self.surface.get_size())
        self.fade_surface.fill(self.fade_color)
    
    def render(self, screen: pygame.Surface) -> bool:
        """Renders the fade effect, Returns True if the fade is finished."""
        self.fade_surface.set_alpha(self.current_alpha)
        if self.fade_type == "in":
            self.fade_in()
            if self.current_alpha >= self.max_alpha:
                return True

        elif self.fade_type == "out":
            self.fade_out()
            if self.current_alpha <= self.max_alpha:
                return True

        elif self.fade_type == "both":
            if not hasattr(self, "fading_in"):
                self.fading_in = True  # tracks if fading in or out

            if self.fading_in:
                self.fade_in()
                if self.current_alpha >= self.max_alpha:  # switch to fade out
                    self.fading_in = False
            else:
                if not self.run_once:
                    self.reached_middle = True
                    self.run_once = True
                self.fade_out()

            if self.current_alpha <= 0:  # finish when alpha is 0 (done fading out)
                return True
            
        else:
            raise ValueError("fade_type must be 'in', 'out', or 'both'")
        
        screen.blit(self.fade_surface, (0, 0))
        return False
    
    def fade_in(self) -> bool:
        """Fades in the screen."""
        if self.current_alpha <= self.max_alpha:  # allow increasing when at `max_alpha`
            self.current_alpha += self.fade_speed
            return False
        else:
            return True
    
    def fade_out(self) -> bool:
        """Fades out the screen."""
        if self.current_alpha >= 0:  # allow decreasing when at 0
            self.current_alpha -= self.fade_speed
            return False
        else:
            return True
            
    def get_current_alpha(self) -> int:
        return self.current_alpha