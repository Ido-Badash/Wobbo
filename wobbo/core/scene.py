import pygame
import logging

class Scene:
    def __init__(self, objects: list):
        self.objects = objects
        
    def handle_event(self, event: pygame.event.Event):
        """Handle events for all objects in the scene."""
        for obj in self.objects:
            obj.handle_event(event)
                     
    def update(self):
        """Update all objects in the scene."""
        for obj in self.objects:
            obj.update()
        
    def render(self, screen: pygame.Surface):
        """Render all objects in the scene."""
        for obj in self.objects:
            obj.render(screen)
            
    def reset(self):
        """Reset all objects in the scene."""        
        for obj in self.objects:
            obj.reset()
            
    def render_mask(self, screen: pygame.Surface):
        """Render the masks for all objects in the scene."""
        for obj in self.objects:
            obj.render_mask(screen)
    
    @staticmethod
    def get_screen_avrg(screen: pygame.Surface) -> int:
        return int((screen.get_width() + screen.get_height())/2)