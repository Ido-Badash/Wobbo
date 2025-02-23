import pygame
from ...core.scene import Scene

class LevelThree(Scene):
    def __init__(self, objects=[]):
        super().__init__(objects)
        self.screen = pygame.display.get_surface()
        
    def handle_event(self, event):
        super().handle_event(event)
    
    def update(self):
        super().update()
    
    def render(self, screen):
        super().render(screen)