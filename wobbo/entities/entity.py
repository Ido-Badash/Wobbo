import pygame
import logging
from wobbo.utils import constants, colors, load_pygame_image

class Entity:
    def __init__(self, x: int, y: int, width: int, height: int,
                 health: int = 100, attack_dmg: int = 10,
                 image: pygame.Surface = None,
                 color: tuple[int, int, int] = None, mask_setcolor: tuple[int, int, int] = colors.TRANSPARENT,
                 name: str = None, gravity: bool = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.attack_dmg = attack_dmg
        self.image = image
        self.color = color
        self.mask_setcolor = mask_setcolor
        self.name = name
        self.gravity = gravity # this is used to determine if the entity should be affected by gravity
            
        self._og_x = x
        self._og_y = y
        self._og_width = width
        self._og_height = height
        self._og_health = health
        self._og_attack_dmg = attack_dmg
        self._og_image = image
        self._og_color = color
        self._og_name = name
        
        if self.image:
            self.update_mask()
        
        self.screen = pygame.display.get_surface()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.can_die = True
        
        # jumping
        self.y_vel = constants.JUMP_HEIGHT
        
        
    def handle_event(self, event: pygame.event.Event):
        """Handle the event."""
        if event.type == pygame.VIDEORESIZE:
            # sets the pos of the entity reletive to the screen width and height
            self.reletive_x, self.reletive_y = self.get_reletive_pos(pygame.display.get_surface())
            self.update_reletive_position(pygame.display.get_surface(), self.reletive_x, self.reletive_y)
    
    def update(self):
        """Update the entity."""        
        if self.gravity:
            if self.y + self.height > 0:
                self.y += constants.GRAVITY_PULL
                
            elif self.y + self.height <= 0:
                self.y = self.screen.get_height() - self.height
            
        self.clamp_position(pygame.display.get_surface())
        self.update_mask()
        
    def render(self, screen: pygame.Surface):
        """Render the entity."""
        if self.health > 0:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if self.image:
                screen.blit(self.image, (self.x, self.y))
            else:
                pygame.draw.rect(screen, self.color, self.rect)
            
    def reset(self):
        """Reset the entity."""
        self.reset_all()
    
    def render_mask(self, screen: pygame.Surface):
        """Render the entity's mask."""
        if self.health > 0:
            screen.blit(self.mask_surf, self.rect.topleft)
    
    # --- position ---
    def clamp_position(self, screen: pygame.Surface):
        """Clamps the entity's position."""
        self.x = max(0, min(self.x, screen.get_width() - self.width))
        self.y = max(0, min(self.y, screen.get_height() - self.height))
        
    def move_x_axis(self, amount: int):
        """Move the entity on the x-axis by the amount."""
        self.x += amount
        
    def move_y_axis(self, amount: int):
        """Move the entity on the y-axis by the amount."""
        self.y += amount
    
    def jump(self):
        """Jump the entity, Returns True if the jump is finished."""
        self.gravity = False
        self.y -= self.y_vel
        self.y_vel -= constants.GRAVITY
        if self.y_vel < -constants.JUMP_HEIGHT:
            self.y_vel = constants.JUMP_HEIGHT
            self.gravity = True
            return True
        return False
    
    # --- actions ---
    def attack_entity(self, entity: "Entity") -> int:
        """Attack another entity and return the entity's health."""
        entity.health -= self.attack_dmg
        return entity.health
    
    def kill(self, reset_after: bool = True):
        """Kills the entity."""
        if self.can_die:
            self.health = 0
            self.reset_all() if reset_after else None
        
    def revive(self):
        """Revive the entity."""
        self.health = self._og_health if self._og_health > 0 else 100
    
    def speak(self, message: str):
        """Print a message from the entity."""
        msg_len = len(message)
        if msg_len > 50:
            logging.warning(f"The message of '{self.name}' is too long: {msg_len} characters, should be less than 50.")
        logging.info(f"{self.name}: {message}")
        # replace later with a pygame text box
        # use the msg_len to determine how long to display the message
        # use time module to do that
        
    # --- state ---
    def is_alive(self) -> bool:
        """Return True if the entity is alive."""
        return self.health > 0
        
    # --- Resets ---
    def reset_rect(self, x: int = None, y: int = None, width: int = None, height: int = None):
        """Reset the rectangle values."""
        self.x = x if x else self._og_x
        self.y = y if y else self._og_y
        self.width = width if width else self._og_width
        self.height = height if height else self._og_height
        
    def reset_specs(self, health: int = None, attack_dmg: int = None, can_die: bool = None):
        """Reset the entity's specs."""
        self.health = health if health else self._og_health
        self.attack_dmg = attack_dmg if attack_dmg else self._og_attack_dmg
        self.can_die = can_die if can_die else True
        
    def reset_apperance(self, image: str = None, color: tuple[int, int, int] = None, name: str = None):
        """Reset the entity's appearance."""
        self.image = load_pygame_image(image, (self.width, self.height)) if image else self._og_image
        self.color = color if color else self._og_color
        self.name = name if name else self._og_name
        
    def reset_all(self):
        """Reset all the entity's values, complete wipe."""
        self.revive()
        self.reset_rect()
        self.reset_specs()
        self.reset_apperance()
        
    # --- Updates ---
    def update_mask(self, threshold: int = 127):
        """Update the entity's mask."""
        if self.image:
            self.mask = pygame.mask.from_surface(self.image, threshold)
            self.mask_surf = self.mask.to_surface(unsetcolor=colors.TRANSPARENT, setcolor=self.mask_setcolor)
            
    def update_reletive_position(self, screen: pygame.Surface, x: float, y: float):
        """Update the entity's position reletive to the screen width and height."""
        self.x = int(x * screen.get_width())
        self.y = int(y * screen.get_height())
        
    # --- set attributes ---                    
    def set_img_alpha(self, alpha: int):
        """Set the image's alpha."""
        self.image.set_alpha(alpha)
        
    def set_size(self, width: int, height: int):
        """Set the entity's size."""
        self.width = width
        self.height = height
        if self.image:
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            
    def set_pos(self, x: int, y: int):
        """Set the entity's position."""
        self.x = x
        self.y = y
        
    # --- get attributes ---
    def get_rect(self) -> pygame.Rect:
        """Return the entity's rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_reletive_pos(self, screen) -> tuple[int, int]:
        """Return the entity's position reletive to the screen width and height."""
        return self.x / screen.get_width(), self.y / screen.get_height()
    
    def __str__(self):
        return f"Entity({self.x}, {self.y}, {self.width}, {self.height},"\
               f"{self.health}, {self.attack_dmg},"\
               f"{self.image}, {self.color}, {self.name})"