# --- Imports ---#
import os
import requests
import logging
from pathlib import Path
from config import TEMP_FOLDER

# --- other shit here --- #

# --- Functions for Main --- #
def download_image(image_url: str) -> Path :
    try :
        TEMP_FOLDER.mkdir(exist_ok=True)  # ensure folder exists
        
        # generate unique filename from URL
        image_name = "wallpaper.bmp"  # fixed name for wallpaper
        image_path = TEMP_FOLDER / image_name

        # send a GET request to the image URL , download the image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # raise an error if bad responses

        # save the image
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        logging.info(f"Image downloaded to {image_path}")
        return image_path

    except Exception as e :
        logging.error(f"Download failed: {e}")
        return Path("")  # return empty path object on error
