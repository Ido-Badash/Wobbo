import pygame
import logging
import colorama

from wobbo.utils import exit_game, logging_setup, catch_it
from wobbo.core.engine import Engine

@catch_it
def main():
    logging_setup(level=logging.DEBUG)
    logging.info("Program started\n")
    colorama.init(autoreset=True)
    
    pygame_init = pygame.init()
    if pygame_init[1] != 0:
        logging.error(f"Pygame failed to initialize: {pygame.get_error()}.")
    pygame.mixer.init()
        
    user_display = pygame.display.Info()
    user_w, user_h = user_display.current_w, user_display.current_h
    screen_flags = pygame.RESIZABLE
    screen = pygame.display.set_mode((user_w/1.25, user_h/1.25), screen_flags)
    
    engine = Engine(screen, user_w/1.75, user_h/1.75, screen_flags=screen_flags)
    engine.run()
    
    logging.info("Program finished")
    exit_game()
    9
if __name__ == "__main__":
    main()
