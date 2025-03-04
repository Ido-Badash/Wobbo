import pygame
import logging
from wobbo.utils import constants, colors, load_pygame_image

class Entity:
    def __init__(self, x: int, y: int, width: int, height: int,
                 health: int = 100, attack_dmg: int = 10,
                 image: pygame.Surface = None,
                 color: tuple[int, int, int] = None,
                 name: str = None, active: bool = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.attack_dmg = attack_dmg
        self.image = image
        self.color = color
        self.name = name
        self.active = active # this is used to times where the entity cant be moved, like the pause menu
        
        self._og_x = x
        self._og_y = y
        self._og_width = width
        self._og_height = height
        self._og_health = health
        self._og_attack_dmg = attack_dmg
        self._og_image = image
        self._og_color = color
        self._og_name = name
        self._og_active = active
        
        if self.image:
            self.image.set_colorkey(colors.BLACK)
            self.mask = pygame.mask.from_surface(self.image)
        
        self.screen = pygame.display.get_surface()
        
        # jumping
        self.active_gravity = True
        self.JUMP_HEIGHT = 10
        self.Y_VELOCITY = self.JUMP_HEIGHT
        
    def handle_event(self, event: pygame.event.Event):
        """Handle the event."""
        if event.type == pygame.VIDEORESIZE:
            # sets the pos of the entity reletive to the screen width and height
            self.relative_x = self.x/self.screen.get_width()
            self.relative_y = self.y/self.screen.get_height() if self.y == self.height else self.height
            self.update_reletive_position(pygame.display.get_surface())
    
    def update(self):
        """Update the entity."""
        if self.health <= 0:
            self.kill()
        
        if self.active_gravity:
            if self.y + self.height > 0:
                self.y += constants.GRAVITY
            
        self.clamp_position(pygame.display.get_surface())
        
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
        pass
    
    def render_mask(self, screen: pygame.Surface):
        """Render the entity's mask."""
        screen.blit(self.mask.to_surface(setcolor=colors.RED, unsetcolor=colors.TRANSPARENT), self.rect.topleft)
    
    # --- position ---
    def clamp_position(self, screen: pygame.Surface):
        """Clamps the entity's position."""
        self.x = max(0, min(self.x, screen.get_width() - self.width))
        self.y = max(0, min(self.y, screen.get_height() - self.height))
        
    def update_reletive_position(self, screen: pygame.Surface):
        """Update the entity's position reletive to the screen width and height."""
        self.x = screen.get_width() * self.relative_x
        self.y = screen.get_height() * self.relative_y
        
    def move_x_axis(self, amount: int):
        """Move the entity on the x-axis by the amount."""
        self.x += amount
        
    def move_y_axis(self, amount: int):
        """Move the entity on the y-axis by the amount."""
        self.y += amount
    
    def jump(self):
        """Jump the entity, Returns True if the jump is finished."""
        self.active_gravity = False
        self.y -= self.Y_VELOCITY
        self.Y_VELOCITY -= constants.GRAVITY
        if self.Y_VELOCITY < -self.JUMP_HEIGHT:
            self.Y_VELOCITY = self.JUMP_HEIGHT
            self.active_gravity = True
            return True
        return False
    
    # --- actions ---
    def attack_entity(self, entity: "Entity") -> int:
        """Attack another entity and return the entity's health."""
        entity.health -= self.attack_dmg
        return entity.health
    
    def kill(self):
        """Kills the entity."""
        self.health = 0
        
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
        
    def deactive(self):
        """Deactivate the entity."""
        self.active = False
        
    def activate(self):
        """Activate the entity."""
        self.active = True
        
    # --- Resets ---
    def reset_rect(self, x: int = None, y: int = None, width: int = None, height: int = None):
        """Reset the rectangle values."""
        self.x = x if x else self._og_x
        self.y = y if y else self._og_y
        self.width = width if width else self._og_width
        self.height = height if height else self._og_height
        
    def reset_specs(self, health: int = None, attack_dmg: int = None):
        """Reset the entity's specs."""
        self.health = health if health else self._og_health
        self.attack_dmg = attack_dmg if attack_dmg else self._og_attack_dmg
        
    def reset_apperance(self, image: str = None, color: tuple[int, int, int] = None, name: str = None):
        """Reset the entity's appearance."""
        self.image = load_pygame_image(image, (self.width, self.height)) if image else self._og_image
        self.color = color if color else self._og_color
        self.name = name if name else self._og_name
        
    def reset_state(self, active: bool = None):
        """Reset the entity's state."""
        self.active = active if active else self._og_active
        
    def reset_all(self):
        """Reset all the entity's values, complete wipe."""
        self.reset_rect()
        self.reset_specs()
        self.reset_apperance()
        self.reset_state()
        
    # --- set attributes ---
    def set_attributes(self, **kwargs):
        """Set the attributes of the entity."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __str__(self):
        return f"Entity({self.x}, {self.y}, {self.width}, {self.height},"\
               f"{self.health}, {self.attack_dmg},"\
               f"{self.image}, {self.color}, {self.name})"