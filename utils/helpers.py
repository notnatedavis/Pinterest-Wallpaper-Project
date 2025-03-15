# --- Imports ---#
import os
import logging
import random

# --- other shit here --- #

# --- Functions for Main --- #
def validate_paths(source: str, destination: str, temp_folder: str) : 
    # validates whether source & destination paths exist + temp folder dir

    # validate source path
    if not os.path.exists(source) :
        logging.error(f"Source path doesn't exist : {source}")
        raise FileNotFoundError(f"Source path doesn't exist : {source}")
    
    # validate destination path
    if not os.path.exists(destination) :
        logging.error(f"Destination path doesn't exist : {destination}")
        raise FileNotFoundError(f"Destination path doesn't exist : {destination}")
    
    # temporary folder creation
    if not os.path.exists(temp_folder) : 
        logging.info(f"Creating temporary folder : {temp_folder}")
        os.makedirs(temp_folder)
    
    logging.info("Paths validated")

def randomly_select_image(image_urls: list) -> str :
    # randomly selects and returns an image URL from the list.

    if not image_urls:
        raise ValueError("No image URLs available to select from.")
    
    return random.choice(image_urls)
