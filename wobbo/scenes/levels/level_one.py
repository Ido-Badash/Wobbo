import pygame
from wobbo.core import Scene
from wobbo.ui import Text, render_fade_out_text
from wobbo.utils import constants, colors

class Level1(Scene):
    def __init__(self, objects=[]):
        super().__init__(objects)
        self.screen = pygame.display.get_surface()
        self.title_font_size = int(self.get_screen_avrg(self.screen) * constants.LEVEL_TITLE_SIZE_FACTOR)
        self.title_font = pygame.font.Font(constants.GAME_FONT, self.title_font_size)
        self.title = Text("Level 1", self.title_font, colors.WHITE)
        self.title_fade_effect = True
    
    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)
        if event.type == pygame.VIDEORESIZE:
            self.title_font_size = int(self.get_screen_avrg(self.screen) * constants.LEVEL_TITLE_SIZE_FACTOR)
            self.title_font = pygame.font.Font(constants.GAME_FONT, self.title_font_size)
            self.title.font = self.title_font
    
    def update(self):
        super().update()
        self.title.update()
    
    def render(self, screen: pygame.Surface):
        super().render(screen)
        screen.fill((255, 0, 0))
        self.render_title(screen)
        
    def reset(self):
        super().reset()
        self.title.alpha = 255
        self.title_fade_effect = True
        self.title_start_fade_timer = pygame.time.get_ticks()
        
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