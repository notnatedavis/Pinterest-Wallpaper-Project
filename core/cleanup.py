# --- Imports ---#
import os
import shutil
import logging

# --- other shit here --- #

# --- Functions for Main --- #
def cleanup_temp_files(temp_folder: str) :
    # deletes temporary files to keep the system clean.

    # only clean up if there are files in the temp folder
    if os.path.exists(temp_folder) and os.listdir(temp_folder):
        shutil.rmtree(temp_folder) # commented out to see functionality
        logging.info(f"Temporary folder '{temp_folder}' cleaned up.")
    else:
        logging.info(f"No files to clean up in '{temp_folder}'.")

    # use shutil.rmtree() directly on the folder without checking because who gives a fuck
