# main.py
# --- Imports ---#
import logging
from utils.logger import logger
from config import PRESET_SOURCE, PRESET_DESTINATION, TEMP_FOLDER
from utils.helpers import validate_paths, ensure_temp_folder, randomly_select_image
from core.cleanup import cleanup
from core.fetcher import fetch_board  # Updated import
from core.downloader import download_image
from core.wallpaper import set_wallpaper
from gui.tkinterWindow import open_window

# --- Helper Functions --- #
def perform_initial_setup() -> None:
    """Validate system paths and create required directories"""
    validate_paths(PRESET_SOURCE, PRESET_DESTINATION)
    ensure_temp_folder(TEMP_FOLDER)
    logger.debug("System paths validated and temp folder ensured")

def update_wallpaper(pinterest_url: str) -> None:
    """Handles complete wallpaper update workflow using fetch_board"""
    try:
        # Validate essential paths
        validate_paths(PRESET_SOURCE, PRESET_DESTINATION)

        # Fetch and process Pinterest data using renamed function
        board = fetch_board(pinterest_url)
        
        if not board.pins:
            logger.warning("No pins found on Pinterest board")
            return

        # Select and download image
        selected_pin = randomly_select_image(board.pins)
        image_path = download_image(selected_pin.image_url)

        if not image_path.exists():
            logger.error("Downloaded image file not found")
            return

        # Apply new wallpaper
        set_wallpaper(image_path)
        logger.info("Wallpaper updated successfully")
        
    except Exception as e:
        logger.error(f"Update failed: {str(e)}", exc_info=True)
        raise

# --- Main Function --- #
def main() -> None:
    try:
        logger.info("Starting Pinterest-Wallpaper-Engine")
        
        # 1. Perform initial system checks
        perform_initial_setup()
        
        # 2. Launch GUI - handles processing through its own interface
        open_window()  # Main processing happens here
        
        logger.info("Application shutdown initiated")

    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        raise
    finally:
        cleanup()
        logger.info("Cleanup completed")

if __name__ == "__main__":
    main()
