import logging
import colorama

from wobbo.utils import exit_game, logging_setup, catch_it
from wobbo.core.engine import Engine


@catch_it
def main():
    logging_setup(level=logging.DEBUG)
    logging.info("Program started\n")
    colorama.init(autoreset=True)
    engine = Engine(800, 600, 60)
    engine.run()
    logging.info("Program finished")
    exit_game()
    
if __name__ == "__main__":
    main()
