# --- Imports ---#
import ctypes
import platform
import subprocess
import logging
from core.validation import validate_and_preprocess_image

# --- other shit here --- #

# --- Functions for Main --- #
def set_wallpaper(image_path: str) :
    # sets the given image as the desktop wallpaper based on the OS.

    try:
        # validate image and preprocess if necessary
        image_path = validate_and_preprocess_image(image_path)
        if not image_path:
            logging.error("Image validation failed. Wallpaper not set.")
            return

        os_name = platform.system()

        # OS selection
        if os_name == "Windows":
            # constants for setting wallpaper
            SPI_SETDESKWALLPAPER = 20  # action
            SPIF_UPDATEINIFILE = 0x01  # update user
            SPIF_SENDWININICHANGE = 0x02  # notify

            # call windows API for wallpaper
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, image_path,
                SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
            )
            logging.info(f"Wallpaper set to: {image_path} (Windows)")

        elif os_name == "Darwin":  # macOS
            # AppleScript via subprocess
            # TRIPLE CHECK (doesnt work ?)
            script = f"""
                tell application "System Events"
                set picture of every desktop to "{image_path}"
                end tell"""
                
            subprocess.run(["osascript", "-e", script], check=True)
            logging.info(f"Wallpaper set to: {image_path} (macOS)")

        else:
            logging.warning("Unsupported operating system. Wallpaper not set.")

    except Exception as e:
        logging.error(f"Error setting wallpaper: {e}")
