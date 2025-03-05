import os
import pygame
from wobbo.utils import load_pygame_image, constants

def load_assets():
    """Loads all assets, except for fonts."""
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    images = {
        "player": {
            "idle": load_pygame_image(f"{assets_dir}/images/player/idle.png", constants.PLAYER_SIZE),
            "star": load_pygame_image(f"{assets_dir}/images/player/star.png", constants.PLAYER_SIZE),
        },
        "star": {
            "idle": load_pygame_image(f"{assets_dir}/images/star/idle.png", constants.STAR_SIZE),
        },
        "tutorial": {
            "course": load_pygame_image(f"{assets_dir}/images/tutorial/course.png", (800, 800)),
        }
    }
    sounds = {
        "star": {
            "pickup": pygame.mixer.Sound(f"{assets_dir}/audio/sfx/star_pickup.mp3"),
        },
    }
    
    assets = {
        "images": images,
        "sounds": sounds,
    }
    
    return assets