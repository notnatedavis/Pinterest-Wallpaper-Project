# core/cleanup.py
# --- Imports ---#
import os
import time
import shutil
import logging
import platform
from pathlib import Path
from config import TEMP_FOLDER

# --- other shit here --- #

# --- Functions for Main --- #
def cleanup() -> None :
    # forcefully removes temp_images folder
    try :
        if TEMP_FOLDER.exists() :
            shutil.rmtree(TEMP_FOLDER, ignore_errors=True)
            logging.info(f"Deleted temp folder: {TEMP_FOLDER}")
            
        # freate fresh folder (optional)
        # TEMP_FOLDER.mkdir(exist_ok=True) # marked out (not needed atm)
        
    except Exception as e:
        logging.error(f"Cleanup error: {str(e)}")
