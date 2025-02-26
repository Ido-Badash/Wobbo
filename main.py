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
    user_display = pygame.display.Info()
    user_w, user_h = user_display.current_w, user_display.current_h
    fps = 60
    engine = Engine(user_w / 2, user_h / 2, fps)
    engine.run()
    logging.info("Program finished")
    exit_game()
    
if __name__ == "__main__":
    main()
