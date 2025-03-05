from .entity import Entity
import pygame

class Npc(Entity):
    """A non-playable character."""
    def __init__(self):
        pass
    
    def handle_event(self, event: pygame.event.Event):
        pass
    
    def update(self):
        pass
    
    def render(self, screen: pygame.Surface):
        pass
    
    def reset(self):
        pass

    def render_mask(self, screen):
        pass