import pygame
import logging
from .scene_manager import SceneManager
from .scene import Scene
import wobbo.scenes as scenes
from wobbo.utils import constants, check_idx_in_range, color_up

class Engine:
    def __init__(self, width, height, fps):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Wobbo")
        
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True    
        
        # Menus
        exit_menu = scenes.ExitMenu()
        main_menu = scenes.MainMenu()
        
        # Tutorial
        tutorial = scenes.Tutorial()
        
        # Levels
        level_1 = scenes.Level1()
        level_2 = scenes.Level2()
        level_3 = scenes.Level3()
        
        # Effects
        self.fade_effect = scenes.Fade(self.screen, 10)
        self.fade_scene_move = None
        self.start_fade_effect = False
        self.move_close_scene = "next"
        
        # Scenes Setup
        self.scene_manager = SceneManager()
        
        all_scenes = [main_menu, exit_menu, tutorial, level_1, level_2, level_3]
        for scene in all_scenes:
            self.scene_manager.add_scene(scene)
        self.scene_manager.set_scene(tutorial)
        
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.scene_manager.update()
            self.scene_manager.render(self.screen)   
            self.fade_transition(self.fade_scene_move)
            pygame.display.flip()
            self.clock.tick(self.fps)

    def handle_events(self):
        """Handle all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                # --- Admin Keys ---
                if constants.RUN_AS_ADMIN:
                    # the `and not self.start_fade_effect` is to avoid
                    # moving to another scene while the fade effect is running
                    if event.key == pygame.K_n and not self.start_fade_effect:
                        if check_idx_in_range(self.scene_manager.get_next_scene_idx(), self.scene_manager.scenes):
                            logging.debug(f"Moving to the next scene '{self.scene_manager.get_next_scene().__class__.__name__}'")
                            self.move_close_scene = "next"
                            self.start_fade_effect = True
                            
                    if event.key == pygame.K_p and not self.start_fade_effect:
                        if check_idx_in_range(self.scene_manager.get_previous_scene_idx(), self.scene_manager.scenes):
                            logging.debug(f"Moving to the previous scene '{self.scene_manager.get_previous_scene().__class__.__name__}'")
                            self.move_close_scene = "previous"
                            self.start_fade_effect = True
                    
            self.scene_manager.handle_event(event)
            
    def move_to_scene(self, scene: Scene):
        """Move to a specific scene, with a fade effect."""
        logging.debug(f"Moving to the scene '{scene.__class__.__name__}'")
        self.fade_transition(scene)
            
    def fade_transition(self, to_scene: Scene):
        """Transition between scenes using a fade effect."""
        if self.start_fade_effect:
            self.fade_effect.update()
            finished_fade = self.fade_effect.render(self.screen)
            if self.fade_effect.reached_middle:
                if self.move_close_scene == "next":
                    scene = self.scene_manager.get_next_scene()
                elif self.move_close_scene == "previous":
                    scene = self.scene_manager.get_previous_scene()
                else:
                    if to_scene is not None:
                        scene = to_scene
                    else:
                        logging.error(color_up("No scene provided to move to, using the current scene."))
                        scene = self.scene_manager.get_current_scene() 
                    
                self.scene_manager.set_scene(scene)
                self.fade_effect.reached_middle = False
                
            if finished_fade:
                self.start_fade_effect = False
                self.fade_effect.reset()