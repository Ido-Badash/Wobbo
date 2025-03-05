import pygame
import logging
from functools import wraps
from .scene import Scene
from wobbo.utils import color_up, exit_game, check_idx_in_range
from wobbo.scenes.effects import Fade

def is_current_scene(custom_error_msg: str = None, custom_error_tip: str = None, exit_upon_error: bool = True):
    """Decorator to check if a current scene is set."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.current_scene is None:
                msg = custom_error_msg or f"Cannot perform `{func.__name__}` operation because no current scene is set."
                tip = custom_error_tip or None
                logging.error(color_up(msg))
                logging.error(color_up(tip)) if tip else None
                exit_game(1) if exit_upon_error else None
            else:
                return func(self, *args, **kwargs)
        return wrapper
    return decorator

class SceneManager:
    def __init__(self):
        self.scenes: list[Scene] = []
        self.current_scene = None
    
    @is_current_scene()
    def handle_event(self, event: pygame.event.Event):
        """Handle events for all scenes, a scene must have a handle_event method."""
        self.current_scene.handle_event(event)
    
    @is_current_scene()
    def manage_scene(self, engine):
        """Manage all scenes, this method is optional for a scene."""
        if hasattr(self.current_scene, "manage_scene"):
            self.current_scene.manage_scene(self, engine)
    
    @is_current_scene()
    def update(self):
        """Update all scenes, a scene must have an update method."""
        self.current_scene.update()
    
    @is_current_scene()
    def render(self, screen: pygame.Surface):
        """Render all scenes, a scene must have a render method."""
        self.current_scene.render(screen)
    
    @is_current_scene()
    def reset(self):
        """Reset all scenes, a scene must have a reset method."""
        self.current_scene.reset()
    
    @is_current_scene()
    def render_mask(self, screen: pygame.Surface):
        """Render the masks for all scenes, a scene must have a render_mask method."""
        self.current_scene.render_mask(screen)  
        
    # --- Scene Management ---
    def set_scene(self, scene: Scene):
        """Set the current scene, scene must be a Scene object."""
        self.current_scene = scene
        self.current_scene.reset()
        
    def add_scene(self, scene):
        """Add a scene to the scene manager, scene must be a Scene object."""
        self.scenes.append(scene)
        
    def delete_scene(self, scene):
        """Delete a scene from the scene manager, scene must be a Scene object."""
        self.scenes.remove(scene)
    
    # --- Scene Navigation ---
    @is_current_scene()
    def get_current_scene(self) -> Scene | None:
        """Return the current scene, in the form of a Scene object."""
        return self.current_scene
    
    def get_next_scene(self) -> Scene | None:
        """Returns the next scene as a `Scene` object."""
        next_index = self.get_next_scene_idx()
        # makes sure that `next_index` is in range of `len(self.scenes)`
        if check_idx_in_range(next_index, self.scenes):
            return self.scenes[next_index]
        else:
            logging.error(color_up("Cannot get the next scene because the current scene is the last one."))
            return None
      
    def get_previous_scene(self) -> Scene | None:
        """Returns the previous scene as a `Scene` object."""
        previous_index = self.get_previous_scene_idx()
        # makes sure that `previous_scene` is in range of `len(self.scenes)`
        if check_idx_in_range(previous_index, self.scenes):
            return self.scenes[previous_index]
        else:
            logging.error(color_up("Cannot get the previous scene because the current scene is the first one."))
            return None
                
    def next_scene(self):
        """Set the next scene as the current scene."""
        if self.current_scene is not None:
            self.set_scene(self.get_next_scene())
        else:
            logging.error(color_up("There is no next scene to move to."))
        
    def previous_scene(self):
        """Set the previous scene as the current scene."""
        if self.current_scene is not None:
            self.set_scene(self.get_previous_scene())
        else:
            logging.error(color_up("There is no previous scene to move to."))
    
    # --- Get Scene Indexes ---
    def get_current_scene_idx(self) -> int:
        """Return the index of the current scene, Returns -1 if no current scene is set."""
        if self.current_scene is None:
            return -1
        return self.scenes.index(self.get_current_scene())
    
    def get_next_scene_idx(self) -> int:
        """Return the index of the next scene, Returns -1 if no next scene is set."""
        if self.current_scene is None:
            return -1
        return self.get_current_scene_idx() + 1
    
    def get_previous_scene_idx(self) -> int:
        """Return the index of the previous scene, Returns -1 if no previous scene is set."""
        if self.current_scene is None:
            return -1
        return self.get_current_scene_idx() - 1
    
    # --- Get Scene Length ---
    def get_scenes_len(self) -> int:
        """Return the number of scenes in the scene manager."""
        return len(self.scenes)