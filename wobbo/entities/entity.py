import time
import pygame
import logging
from ..utils.helpers import load_pygame_image

class Entity:
    def __init__(self, x: int, y: int, width: int, height: int,
                 health: int = 100, attack: int = 10,
                 image: str = None,
                 color: tuple[int, int, int] = None,
                 name: str = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.attack = attack
        self.image = load_pygame_image(image, (width, height)) if image else None
        self.color = color
        self.name = name
        
        self.junped = False
        
    def handle_event(self, event: pygame.event.Event):
        pass
    
    def update(self):
        if self.health <= 0:
            self.kill()
        
    def render(self, screen: pygame.Surface):
        if self.image and self.image_size:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def move_x_axis(self, amount: int):
        """Move the entity on the x-axis by the amount."""
        self.x += amount
        
    def move_y_axis(self, amount: int):
        """Move the entity on the y-axis by the amount."""
        self.y += amount
        
    def attack(self, entity: "Entity") -> int:
        """Attack another entity and return the entity's health."""
        entity.health -= self.attack
        return entity.health
    
    def speak(self, message: str):
        """Print a message from the entity."""
        msg_len = len(message)
        logging.info(f"{self.name}: {message}")
        # replace later with a pygame text box
        # use the msg_len to determine how long to display the message
        # use time module to do that
    
    def kill(self):
        """Kills the entity."""
        self.health = 0
        self.x = -1000
        self.y = -1000
        self.width = 0
        self.height = 0
        self.image = None
        self.image_size = None
        self.color = None
        self.name = None
        
    def revive(self, x: int, y: int, width: int, height: int,
               health: int = 100, attack: int = 10,
               image: str = None, image_size: tuple[int, int] = None,
               color: tuple[int, int, int] = None,
               name: str = None):
        """Revive the entity with new parameters."""
        return Entity(x, y, width, height, health, attack, image, image_size, color, name)
    
    def __str__(self):
        return f"Entity({self.x}, {self.y}, {self.width}, {self.height}, {self.health}, {self.attack}, {self.image}, {self.image_size}, {self.color}, {self.name})"