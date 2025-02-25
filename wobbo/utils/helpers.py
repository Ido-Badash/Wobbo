import os
import sys
import pygame
import logging
from colorama import Fore, Back, Style

def exit_game(exit_code=0):
    """Exit the game and log a message."""
    pygame.quit()
    sys.exit(exit_code)
    
def path_exists(image_path):
    """Check if the image path exists."""
    formatted_image_path = os.path.normpath(image_path)
    if not os.path.exists(formatted_image_path):
        logging.error(f"Image path does not exist: {formatted_image_path}")
        raise FileNotFoundError(f"Image path does not exist: {formatted_image_path}")
    return formatted_image_path
    
def load_pygame_image(image_path: str, image_size: tuple[int, int]) -> pygame.Surface:
    """Load an image using pygame and return it."""
    image_path = path_exists(image_path)
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, image_size)
    return image

def color_up(msg: str, fore: str = Fore.RED,
             style: str = Style.NORMAL, back: str = Back.RESET):
    """Return a colored message."""
    return f"{fore}{style}{back}{msg}{Back.RESET}{Style.RESET_ALL}{Fore.RESET}"\
        if back\
        else f"{fore}{style}{msg}{Style.RESET_ALL}{Fore.RESET}"

# --- Math Helpers ---
def check_idx_in_range(num: float | int, data):
    """Check if the index is in range of the data."""
    return 0 <= num < len(data)