# --- Imports ---#
import os
import requests
import logging

# --- other shit here --- #

# --- Functions for Main --- #
def download_image(image_url: str, save_path: str) -> str :
    try:
        # send a GET request to the image URL
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # raise an error if bad responses

        # create a file name from the URL (update in the future for better readability)
        image_name = image_url.split("/")[-1]

        # full path to save the image
        image_path = os.path.join(save_path, image_name)

        # write the image to the file (w/ Pillow)
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):  # save in chunks
                file.write(chunk)

        logging.info(f"Image downloaded and saved to {image_path}")
        return image_path

    except Exception as e :
        logging.error(f"Error downloading image: {e}")
        return ""