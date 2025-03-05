import json
import pygame
import logging
from .entity import Entity
from wobbo.core.assets_loader import load_assets
from wobbo.utils import colors, constants

class Player(Entity):
    def __init__(self, x: int, y: int, width: int = constants.PLAYER_SIZE[0], height: int = constants.PLAYER_SIZE[1]):
        self.screen = pygame.display.get_surface()
        self.PLAYER_ASSETS = load_assets()["images"]["player"]
        self._og_x = x
        self._og_y = y
        self.width = width
        self.height = height
        self.color = colors.WHITE
        self.name ="Wobbo"
        self.image = self.PLAYER_ASSETS["idle"]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.active_plr = True
        super().__init__(x, y, self.width, self.height, image=self.image,
                         color=self.color, mask_setcolor=colors.PLAYER, name=self.name)
        
        # Images and masks
        self.right_img = self.image
        self.left_img = pygame.transform.flip(self.image, True, False)
        
        # Jumping
        self.jumped = False
                
    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)
        
    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if self.active_plr:
            if keys[pygame.K_a]:
                self.move_x_axis(-constants.X_VELOCITY)
                if self.image:
                    self.image = self.left_img
                
            if keys[pygame.K_d]:
                self.move_x_axis(constants.X_VELOCITY)
                if self.image:
                    self.image = self.right_img
                    
            if keys[pygame.K_w]:
                self.move_y_axis(-constants.Y_VELOCITY)
                if self.image:
                    pass
                
            if keys[pygame.K_s]:
                self.move_y_axis(constants.Y_VELOCITY)
                if self.image:
                    pass
                                
            if keys[pygame.K_SPACE] and self.gravity:
                self.jumped = True
                
            if self.jumped:
                if self.jump():
                    self.jumped = False
        
    def render(self, screen: pygame.Surface):
        super().render(screen)
    
    def reset(self):
        super().reset()
        self.jumped = False
        
    def render_mask(self, screen):
        super().render_mask(screen)
        
    def collision(self, obstacle):
        """The collision between the player and the obstacle."""
        self.kill()
        
    def deactivate(self):
        """Deactivates the player."""
        self.active_plr = False
        
    def activate(self):
        """Activates the player."""
        self.active_plr = True