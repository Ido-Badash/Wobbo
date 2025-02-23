import pygame
from .scene_manager import SceneManager
from ..scenes import *
from ..utils import constants

class Engine:
    def __init__(self, width, height, fps):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Wobbo")
        
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True    
        
        # Menus
        exit_menu = ExitMenu([])
        main_menu = MainMenu([])
        
        # Effects
        self.fade_effect = Fade(self.screen, 1)
        self.start_fade = False
        
        # Scenes Setup
        self.scene_manager = SceneManager()
        
        all_scenes = [main_menu, exit_menu]
        for scene in all_scenes:
            self.scene_manager.add_scene(scene)
        self.scene_manager.set_scene(main_menu)
        
    def run(self):
        """Main game loop."""

        while self.running:
            self.handle_events()
            self.scene_manager.update()
            self.scene_manager.render(self.screen)
            self.fade()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def handle_events(self):
        """Handle all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n and constants.RUN_AS_ADMIN:
                    self.start_fade = True
            self.scene_manager.handle_event(event)
            
    def fade(self):
        """Fade effect handle."""
        if self.start_fade:
            self.fade_effect.update()
            self.finished_fade = self.fade_effect.render(self.screen)
            if self.fade_effect.reached_middle:
                self.screen.fill((0, 0, 0))
                self.scene_manager.next_scene()
                self.fade_effect.reached_middle = False
            if self.finished_fade:
                self.start_fade = False