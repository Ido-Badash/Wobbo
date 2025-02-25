import pygame
from wobbo.core.scene import Scene
from wobbo.ui import Text
from wobbo.utils import constants

class ExitMenu(Scene):
    def __init__(self, objects=[]):
        super().__init__(objects)
        self.screen = pygame.display.get_surface()
        self.text_font = pygame.font.Font(constants.GAME_FONT, 60)
        self.text = Text("Exit Menu", self.text_font, (0, 0, 255))
        self.text_rect = self.text.get_rect()
        
    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)
    
    def update(self):
        super().update()
    
    def render(self, screen: pygame.Surface):
        super().render(screen)
        self.screen.fill((255, 255, 255))
        self.text.render(screen,
                         self.screen.get_width() // 2 - self.text_rect.width // 2,
                         self.screen.get_height() // 2 - self.text_rect.height // 2)