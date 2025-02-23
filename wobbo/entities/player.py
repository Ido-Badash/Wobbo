import pygame
from .entity import Entity
from ..utils.constants import ASSETS

class Player(Entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image: pygame.Surface = ASSETS["images"]["player"]["idle"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.image, self.rect)