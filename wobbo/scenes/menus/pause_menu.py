import pygame
from ...core.scene import Scene

class PauseMenu(Scene):
    def __init__(self, objects=[]):
        super().__init__(objects)
        self.screen = pygame.display.get_surface()
        
    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)
    
    def update(self):
        super().update()
    
    def render(self, screen: pygame.Surface):
        super().render(screen)