# --- Imports ---#
import os
from pathlib import Path

# --- Universal Paths --- #
# get the root directory of project (where config.py is located)
PROJECT_ROOT = Path(__file__).resolve().parent

# define paths relative to the project root
PRESET_SOURCE = PROJECT_ROOT  # Use the project root as the source directory
PRESET_DESTINATION = PROJECT_ROOT  # Use the project root as the destination directory

TEMP_FOLDER = PROJECT_ROOT / "temp_images"

# ensure the temp folder exists
# TEMP_FOLDER.mkdir(parents=True, exist_ok=True)

# specific variables
SCROLL_LIMIT = 20 # remove ?
SLEEP_TIME = 1.5 # update ?

# --- other shit here --- #
