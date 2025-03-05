import os
import json
import psutil
import pygame
import logging
from .scene import Scene
from .scene_manager import SceneManager
from wobbo.ui import Text
import wobbo.scenes as scenes
from wobbo.utils import constants, colors, check_idx_in_range, color_up, find_avrg

class Engine:
    def __init__(self, screen: pygame.Surface, min_width=None, min_height=None, caption: str = "Wobbo", screen_flags: int = 0):
        self.screen = screen
        pygame.display.set_caption(caption)
        self.screen_flags = screen_flags
        
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.min_width = min_width
        self.min_height = min_height
        
        self.settings = json.loads(open("wobbo/config/settings.json").read())
        self.clock = pygame.time.Clock()
        self.fps = self.settings["screen"]["fps"]
        self.running = True   
        
        # Scene Manager
        self.scene_manager = SceneManager() 
        
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
        
        # Game specs
        self.process = psutil.Process(os.getpid())
        self.specs_font_size = self._update_spec_size()
        self.specs_font = pygame.font.Font(constants.GAME_FONT, self.specs_font_size)
        self.memory = Text("", self.specs_font, colors.WHITE, 50)
        self.current_fps = Text("", self.specs_font, colors.WHITE, 50)
        self.spec_time_jump = 1000
        
        # Masks
        self.show_masks = False
        
        # Scenes Setup        
        all_scenes = [main_menu, exit_menu, tutorial, level_1, level_2, level_3]
        for scene in all_scenes:
            self.scene_manager.add_scene(scene)
            
        self.scene_manager.set_scene(tutorial)
        
    def run(self):
        """Main game loop."""
        while self.running:
            self.specs_timer = pygame.time.get_ticks()
            self.handle_events()
            self.scene_manager.manage_scene(self)
            self.scene_manager.update()
            self.scene_manager.render(self.screen)  
            self.scene_manager.render_mask(self.screen) if self.show_masks else None
            self.fade_transition(self.fade_scene_move)

            # --- Display the game specs ---
            # fps
            if self.settings["screen"]["show_fps"] or constants.RUN_AS_ADMIN:
                self.current_fps.set_text(f"FPS: {int(self.clock.get_fps())}")
                self.specs_font_size = self._update_spec_size()
                self.current_fps.set_font(self.specs_font)
                self.current_fps.render(self.screen, 10, 50)
            
            # memory 
            if self.settings["screen"]["show_memory"] or constants.RUN_AS_ADMIN:
                self.memory_bytes = self.process.memory_info().rss
                self.memory.set_text(f"Memory: {self.memory_bytes / (1024 ** 2):.2f} MB")
                self.specs_font_size = self._update_spec_size()
                self.memory.set_font(self.specs_font)
                self.memory.render(self.screen, 10, 10)
            
            pygame.display.flip() # updates the display
            self.clock.tick(self.fps)

    def handle_events(self):
        """Handle all events."""
        for event in pygame.event.get():
            mods = pygame.key.get_mods()
            if event.type == pygame.QUIT:
                self.running = False
            
            # --- Min width and height of screen ---
            if event.type == pygame.VIDEORESIZE:
                screen_w, screen_h = self.screen.get_size()
                screen_w = max(screen_w, self.min_width)
                screen_h = max(screen_h, self.min_height)
                self.screen = pygame.display.set_mode((screen_w, screen_h), self.screen_flags)
                
            if event.type == pygame.KEYDOWN:
                # --- Admin Keys ---
                if constants.RUN_AS_ADMIN:
                    # the `and not self.start_fade_effect` is to avoid
                    # moving to another scene while the fade effect is running
                    if event.key == pygame.K_n and mods & pygame.KMOD_CTRL and not self.start_fade_effect:
                        if check_idx_in_range(self.scene_manager.get_next_scene_idx(), self.scene_manager.scenes):
                            self.move_to_scene(self.scene_manager.get_next_scene())
                            
                    if event.key == pygame.K_p and mods & pygame.KMOD_CTRL and not self.start_fade_effect:
                        if check_idx_in_range(self.scene_manager.get_previous_scene_idx(), self.scene_manager.scenes):
                            self.move_to_scene(self.scene_manager.get_previous_scene())
                            
                    if event.key == pygame.K_m and mods & pygame.KMOD_CTRL:
                        self.show_masks = not self.show_masks
                    
            self.scene_manager.handle_event(event)

    def _update_spec_size(self) -> int:
        """Update the font size of the game specs."""
        new_spec_font_size = int(find_avrg(
                self.screen.get_width(),
                self.screen.get_height(),
                factor=constants.SPECS_TEXT_SIZE_FACTOR
                ))
        return new_spec_font_size
        
    def move_to_scene(self, scene: Scene):
        """Move to a specific scene, with a fade effect."""
        logging.debug(f"Moving to the scene '{scene.__class__.__name__}'")
        self.start_fade_effect = True
        self.fade_scene_move = scene
        
    def fade_transition(self, to_scene: Scene):
        """Transition between scenes using a fade effect."""
        if self.start_fade_effect:
            self.start_fade_effect = not self.transition(to_scene, self.fade_effect, self.start_fade_effect)
            
    def transition(self, to_scene: Scene, effect: scenes.Fade, flag) -> bool:
        """Transition between scenes using an effect, returns True when the transition is finished."""
        if flag:
            effect.update()
            finished_fade = effect.render(self.screen)
            if effect.reached_middle:
                if to_scene is not None:
                    scene = to_scene
                else:
                    logging.error(color_up("No scene provided to move to, using the current scene."))
                    scene = self.scene_manager.get_current_scene() 
                    
                self.scene_manager.set_scene(scene)
                effect.reached_middle = False
                
            if finished_fade:
                flag = False
                effect.reset()
                return True
        return False