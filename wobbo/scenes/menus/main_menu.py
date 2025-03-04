import pygame
from wobbo.core import Scene

class MainMenu(Scene):
    def __init__(self, objects=[]):
        super().__init__(objects)

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)
        
    def update(self):
        super().update()
    
    def render(self, screen: pygame.Surface):
        super().render(screen)
        screen.fill((255, 255, 0))
        
    def reset(self):
        super().reset()