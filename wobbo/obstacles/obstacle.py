import pygame
from wobbo.utils import colors

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def handle_collision(self, player):
        pass
    
    def handle_event(self, event):
        pass
        
    def update(self):
        pass
    
    def render(self, screen: pygame.Surface):
        pass
        
    def reset(self):
        pass
    
    def render_mask(self, screen: pygame.Surface):
        pass