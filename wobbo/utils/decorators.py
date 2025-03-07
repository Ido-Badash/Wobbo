import logging
import traceback
from functools import wraps
from .helpers import exit_game

def catch_it(func):
    """Decorator to catch exceptions and log them."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            logging.error(traceback.format_exc())
            exit_game(1)
    return wrapper
