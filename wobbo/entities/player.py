import json
import pygame
import logging
from .entity import Entity
from wobbo.core.assets_loader import ASSETS
from wobbo.utils import colors, constants

class Player(Entity):
    def __init__(self, x: int, y: int, width: int = constants.PLAYER_SIZE[0], height: int = constants.PLAYER_SIZE[1]):
        self.screen = pygame.display.get_surface()
        self._og_x = x
        self._og_y = y
        self.width = width
        self.height = height
        self.color = colors.WHITE
        self.name ="Wobbo"
        self.image = ASSETS["images"]["player"]["idle"]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        super().__init__(x, y, self.width, self.height, image=self.image, color=self.color, name=self.name)
        
        self.right_plr_image = self.image
        self.left_plr_image = pygame.transform.flip(self.image, True, False)
        self.jumped = False
                
    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            pass    
        
    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.move_x_axis(-constants.X_VELOCITY)
            if self.image:
                self.image = self.left_plr_image
            
        if keys[pygame.K_d]:
            self.move_x_axis(constants.X_VELOCITY)
            if self.image:
                self.image = self.right_plr_image
            
        if keys[pygame.K_SPACE]:
            self.jumped = True
            
        if self.jumped:
            if self.jump():
                self.jumped = False
        
    def render(self, screen: pygame.Surface):
        super().render(screen)
    
    def reset(self):
        self.x = self._og_x
        self.y = self._og_y
        
    def render_mask(self, screen):
        super().render_mask(screen)
        
    def set_size(self, width: int, height: int):
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (width, height))