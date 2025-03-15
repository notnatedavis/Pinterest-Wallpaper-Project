# --- Imports ---#
import time
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
def main() :
    try :
        logger.info("Starting program...")

        # 1. validate paths
        validate_paths(PRESET_SOURCE, PRESET_DESTINATION, TEMP_FOLDER)

        # 2. open Tkinter window
        pinterest_board_url = open_window()
        if not pinterest_board_url :
            logger.error("No valid Pinterest board URL provided. Exiting.")
            return
        
        # 3. fetch Pinterest data from associated url
        board = fetch_pinterest_data(pinterest_board_url)

        if not board.pins :
            logger.warning("No pins found")
            return

        # 4. select and download image
        selected_pin = randomly_select_image(board.pins)
        image_path = download_image(selected_pin.image_url)
        
        if not image_path.exists() :
            logger.error("No image to set")
            return

        # 5. set wallpaper
        set_wallpaper(image_path)
        logger.info("Wallpaper updated successfully")

    except Exception as e :
        logger.error(f"Critical error: {e}", exc_info=True)
        
    finally :
        # 6. always clean up temp files
        time.sleep(1)  # brief pause for system to release locks
        cleanup_temp_files()
        logger.info("Cleanup completed")

if __name__ == "__main__" :
    main()
