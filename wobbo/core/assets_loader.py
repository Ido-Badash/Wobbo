import os
from wobbo.utils import load_pygame_image, constants

def load_assets():
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    images = {
        "player": {
            "idle": load_pygame_image(f"{assets_dir}/images/player/idle.png", constants.PLAYER_SIZE),
        }
    }
    
    assets = {
        "images": images,
    }
    
    return assets

ASSETS = load_assets()