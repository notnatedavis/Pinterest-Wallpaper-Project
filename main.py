# --- Imports ---#
from utils.logger import logger
from config import PRESET_SOURCE, PRESET_DESTINATION, TEMP_FOLDER
from utils.helpers import validate_paths, randomly_select_image
from core.fetcher import fetch_pinterest_data
from core.downloader import download_image
from core.wallpaper import set_wallpaper
from core.cleanup import cleanup_temp_files
from gui.tkinterWindow import open_window

# --- other shit here --- #

# --- Main Function --- #
def main():
    try:
        logger.info("Starting script...")

        # Step 1: Validate paths
        validate_paths(PRESET_SOURCE, PRESET_DESTINATION, TEMP_FOLDER)

        # Step 2: open Tkinter window
        pinterest_board_url = open_window()
        if not pinterest_board_url:
            logger.error("No valid Pinterest board URL provided. Exiting.")
            return
        
        # Step 3: Fetch Pinterest data from associated url
        board = fetch_pinterest_data(pinterest_board_url)

        # Step 4: Randomly select an image and download it
        if board.pins:
            selected_pin = randomly_select_image(board.pins)  # Select a random Pin
            image_path = download_image(selected_pin.image_url, TEMP_FOLDER)

            # Step 5: Set the image as wallpaper
            set_wallpaper(image_path)

            # Step 6: Cleanup temporary files
            cleanup_temp_files(TEMP_FOLDER)
            logger.info("Script execution completed successfully.")
        else:
            logger.warning("No Pins found on the Pinterest board.")
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

# --- Entry Point --- #

if __name__ == "__main__":
    main()
