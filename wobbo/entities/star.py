import logging
import pygame
from . import Entity, Player
from wobbo.core.assets_loader import load_assets
from wobbo.utils import colors, constants

class Star(Entity):
    def __init__(self, x: int, y: int, width: int = constants.STAR_SIZE[0], height: int = constants.STAR_SIZE[1]):
        self.STAR_IMG_ASSETS = load_assets()["images"]["star"]
        self.STAR_AUDIO_ASSETS = load_assets()["sounds"]["star"]
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = colors.LIGHT_BANANA
        self.image = self.STAR_IMG_ASSETS["idle"]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.name = "Lumi"
        super().__init__(x, y, width, height, image=self.image,
                         color=self.color, mask_setcolor=colors.ITEMS, name=self.name)
        
        self.start_pickup_sound = self.STAR_AUDIO_ASSETS["pickup"]
        self.start_pickup_effect = False
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.get_surface()
            self.set_pos(screen.get_width()/1.5, screen.get_height()/5)
    
    def update(self):
        pass
    
    def render(self, screen: pygame.Surface):
        super().render(screen)
    
    def reset(self):
        super().reset()
        self.start_pickup_effect = False
    
    def render_mask(self, screen: pygame.Surface):
        super().render_mask(screen)
        
    def player_pickup(self, player: Player, kill_on_pickup: bool = True, signal_after: int = constants.STAR_PICKUP_EFFECT_START_AFTER):
        """Checks if the player and star masks collide."""
        if self.mask.overlap(player.mask, (int(player.x - self.x), int(player.y - self.y))) and self.health > 0:
            logging.debug("Player picked up the star.")
            if not self.start_pickup_effect:
                self.start_pickup_effect = True
                self.start_timer = pygame.time.get_ticks()
        
        if self.start_pickup_effect:
            timer = pygame.time.get_ticks() - self.start_timer
            player.can_die = False
            self.start_pickup_sound.play()
            player.color = colors.LIGHT_BANANA
            player.image = player.PLAYER_ASSETS["star"]
            player.image = pygame.transform.scale(player.image, (player.width, player.height))
            self.kill(False) if kill_on_pickup else None
            if timer > signal_after:
                # Moves to the next scene after the effect is done
                return True
        return False