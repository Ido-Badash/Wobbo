import pygame
from wobbo.utils import colors
from wobbo.entities import Player

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface = None, color: tuple = None, groups: list = None):
        super().__init__()
        self._og_x = x
        self._og_y = y
        
        self.color = color
        if image is None:
            self.image = pygame.Surface((50, 50))
            self.image.fill(color if self.color else colors.WHITE)
        else:
            self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        self.image.set_colorkey(colors.TRANSPARENT)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_surf = self.mask.to_surface()
        
        if groups:
            if isinstance(groups, pygame.sprite.Group):
                self.add(groups)
            else:
                self.add(*groups) # unpack the list of groups if its not a pygame.sprite.Group
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.get_surface()
            self.update_obstacle_image(screen.get_width(), screen.get_height())
        
    def update(self):
        pass
    
    def render(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect.topleft)
        
    def reset(self):
        self.rect.topleft = (self._og_x, self._og_y)
    
    def render_mask(self, screen: pygame.Surface):
        screen.blit(self.mask.to_surface(), self.rect.topleft)
        
    def handle_collision(self, player: Player):
        if pygame.sprite.collide_mask(self, player):
            player.collision(self)
        
    def calc_offset(self, other_x: int, other_y: int) -> tuple[int, int]:
        return (int(self.x - other_x), int(self.y - other_y))
    
    def update_obstacle_image(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_surf = self.mask.to_surface()
    
    def get_rect(self):
        return self.rect