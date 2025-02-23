import pygame

class Scene:
    def __init__(self, objects: list[object]):
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