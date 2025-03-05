import pygame
from wobbo.core import Scene
from wobbo.core.assets_loader import load_assets
from wobbo.entities import Player, Star
from wobbo.utils import constants, colors
from wobbo.obstacles import Obstacle
from wobbo.ui import Text, render_fade_out_text, render_fade_in_text

class Tutorial(Scene):
    def __init__(self, objects=[]):
        # --- Screen ---
        self.screen = pygame.display.get_surface()
        
        # --- Assets ---
        self.tutorial_assets = load_assets()["images"]["tutorial"]
        
        # --- Entities ---
        # Player
        self.plr = Player(self.screen.get_width() / 3,
                          self.screen.get_height() - constants.PLAYER_SIZE[1])
        self.plr.deactivate()
        
        super().__init__(objects)
        self.screen = pygame.display.get_surface()
        
        # Star
        self.lumi = Star(self.screen.get_width()/1.5,
                         self.screen.get_height()/5)
        self.lumi.set_img_alpha(200)
        self.lumi_picked = False
        
        # --- Obsticles ---
        # Tutorial course
        self.tutorial_assets["course"] = pygame.transform.scale(self.tutorial_assets["course"], (self.screen.get_width(), self.screen.get_height()))
        self.tutorial = Obstacle(0, 0, self.tutorial_assets["course"])
        
        # --- Text ---
        # Title
        self.title_font = pygame.font.Font(constants.GAME_FONT, 0)
        self.title = Text("Tutorial", self.title_font, colors.WHITE)
        
        # Instructions
        self.instructions_font = pygame.font.Font(constants.GAME_FONT, 0)
        self.instructions = Text("Use the 'WASD' keys to move left, right, up and down.",
                                 self.instructions_font, colors.WHITE, 0)
        
        self.objects = [self.lumi, self.plr]
        for obj in objects:
            self.objects.append(obj)
    
    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)
        mods = pygame.key.get_mods()
        if event.type == pygame.KEYDOWN:
            if constants.RUN_AS_ADMIN:
                if event.key == pygame.K_h and mods & pygame.KMOD_CTRL:
                    self.plr.can_die = not self.plr.can_die
        self.tutorial.handle_event(event)
    
    def manage_scene(self, scene_manager, engine):
        if self.lumi_picked and not engine.start_fade_effect:
            engine.move_to_scene(scene_manager.get_next_scene())
    
    def update(self):
        super().update()
        self.title.update()
        self.title.set_font(pygame.font.Font
                            (constants.GAME_FONT,
                            int(self.get_screen_avrg(self.screen, constants.LEVEL_TITLE_SIZE_FACTOR))))
        
        self.instructions.update()
        self.instructions.set_font(pygame.font.Font
                                   (constants.GAME_FONT,
                                    int(self.get_screen_avrg(self.screen) * constants.INSTRUCTIONS_SIZE_FACTOR)))
        
        self.lumi_picked = self.lumi.player_pickup(self.plr)
        self.tutorial.handle_collision(self.plr)
    
    def render(self, screen: pygame.Surface):
        screen.fill(colors.NAVY)
        self.tutorial.render(screen)
        self._render_texts(screen)
        super().render(screen)
        
    def reset(self):
        super().reset()
        self.tutorial.reset()
        self.title.alpha = 255
        self.instructions.alpha = 0
        self.text_start_timer = pygame.time.get_ticks()
        
    def render_mask(self, screen):
        self.tutorial.render_mask(screen)
        super().render_mask(screen)
        
    def _render_texts(self, screen: pygame.Surface):
        """Draws all the texts on the screen."""
        # title
        self.title_x = screen.get_width() / 2 - self.title.get_rect().w / 2
        self.title_y = screen.get_height() / 20
        title_fade_state = render_fade_out_text(screen, self.text_start_timer,
                                  self.title,
                                  (self.title_x, self.title_y),
                                  constants.LEVEL_TITLE_FADE_TIME,
                                  constants.TUTORIAL_FADE_SPEED
                                  )
        
        # instructions
        self.instructions_x = screen.get_width() / 2 - self.instructions.get_rect().w / 2
        self.instructions_y = screen.get_height() / 20
        if title_fade_state:
            self.plr.activate()
            render_fade_in_text(screen, self.text_start_timer,
                                self.instructions,
                                (self.instructions_x, self.instructions_y),
                                fade_speed=constants.INSTRUCTIONS_FADE_SPEED
                                )
        else:
            self.plr.deactivate()
    