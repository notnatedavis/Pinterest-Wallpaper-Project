# --- Imports ---#
import logging

# --- other shit here --- #

# --- Logger Configuration ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set level to INFO, DEBUG, etc.

# console handler to log to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# set log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# add handler to logger
logger.handlers.clear()
logger.addHandler(console_handler)
