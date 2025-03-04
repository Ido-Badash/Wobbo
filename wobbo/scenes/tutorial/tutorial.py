import pygame
import logging
from wobbo.core import Scene
from wobbo.entities import Player
from wobbo.utils import constants, colors
from wobbo.ui import Text, render_fade_out_text

class Tutorial(Scene):
    def __init__(self, objects=[]):
        # Player
        self.screen = pygame.display.get_surface()
        self.plr = Player(self.screen.get_width()/2 - constants.PLAYER_SIZE[0]/2,
                          self.screen.get_height()-constants.PLAYER_SIZE[1])
        
        super().__init__(objects)
        self.screen = pygame.display.get_surface()
        
        # Title
        self.title_font_size = int(self.get_screen_avrg(self.screen) * constants.LEVEL_TITLE_SIZE_FACTOR)
        self.title_font = pygame.font.Font(constants.GAME_FONT, self.title_font_size)
        self.title = Text("Tutorial", self.title_font, colors.WHITE)
        self.title_fade_effect = True
        
        # Masks
        self.show_masks = False
        
        objects.append(self.plr)
    
    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.show_masks = not self.show_masks
    
    def update(self):
        super().update()
        self.title.update()
    
    def render(self, screen: pygame.Surface):
        screen.fill(colors.BLACK)
        self.render_title(screen)
        super().render(screen)
        
    def reset(self):
        super().reset()
        self.title.alpha = 255
        self.title_fade_effect = True
        self.title_start_fade_timer = pygame.time.get_ticks()
        
    def render_mask(self, screen):
        if self.show_masks:
            super().render_mask(screen)
        
    def render_title(self, screen: pygame.Surface):
        """Draws the title on the screen."""
        self.title_x = screen.get_width() / 2 - self.title.get_rect().w / 2
        self.title_y = self.title.get_rect().h / 10
        render_fade_out_text(screen, self.title_start_fade_timer,
                                  self.title,
                                  (self.title_x, self.title_y),
                                  constants.LEVEL_TITLE_FADE_TIME,
                                  constants.LEVEL_TITLE_FADE_SPEED
                                  )