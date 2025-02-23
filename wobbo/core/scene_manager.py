import pygame
import logging
from .scene import Scene
from typing import List
from ..utils import color_up

class SceneManager:
    def __init__(self):
        self.scenes: List[Scene] = []
        self.current_scene = None        
        
    def handle_event(self, event: pygame.event.Event):
        """Handle events for all scenes, a scene must have a handle_event method."""
        if self.current_scene:
            self.current_scene.handle_event(event)
                
    def update(self):
        """Update all scenes, a scene must have an update method."""
        if self.current_scene:
            self.current_scene.update()
            
    def render(self, screen: pygame.Surface):
        """Render all scenes, a scene must have a render method."""
        if self.current_scene:
            self.current_scene.render(screen)
            
    def set_scene(self, scene):
        """Set the current scene, scene must be a Scene object."""
        self.current_scene = scene
            
    def add_scene(self, scene):
        """Add a scene to the scene manager, scene must be a Scene object."""
        self.scenes.append(scene)
        
    def delete_scene(self, scene):
        """Delete a scene from the scene manager, scene must be a Scene object."""
        self.scenes.remove(scene)
        
    def current_scene_index(self) -> int:
        """Return the index of the current scene."""
        return self.scenes.index(self.current_scene)
        
    def next_scene(self):
        """Set the next scene as the current scene."""
        if self.current_scene:
            current_index = self.current_scene_index()
            # makes sure that `current_index` is in range of `len(self.scenes)`
            if current_index + 1 < len(self.scenes):
                self.current_scene = self.scenes[current_index + 1]
            else:
                logging.error(color_up("Cannot move to the next scene because the current scene is the last one."))
        else:
            logging.error(color_up("Cannot move to the next scene because no current scene is set."))

        
    def previous_scene(self):
        """Set the previous scene as the current scene."""
        if self.current_scene:
            current_index = self.current_scene_index()
            # makes sure that `current_index` is in range of `len(self.scenes)`
            if current_index > 0:
                self.current_scene = self.scenes[current_index - 1]
            else:
                logging.error(color_up("Cannot move to the previous scene because the current scene is the first one."))
        else:
            logging.error(color_up("Cannot move to the previous scene because no current scene is set."))