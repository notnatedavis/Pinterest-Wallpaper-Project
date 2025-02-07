# --- Imports ---#
import os
from pathlib import Path

# --- Universal Paths --- #
# Get the root directory of project (where config.py is located)
PROJECT_ROOT = Path(__file__).resolve().parent

# Define paths relative to the project root
PRESET_SOURCE = PROJECT_ROOT  # Use the project root as the source directory
PRESET_DESTINATION = PROJECT_ROOT  # Use the project root as the destination directory

# Temporary folder for downloaded images
TEMP_FOLDER = os.path.join(PROJECT_ROOT, "temp_images")

# Ensure the temp folder exists
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Specific variables
SCROLL_LIMIT = 3 # remove ?
SLEEP_TIME = 3 # update ?

# --- other shit here --- #