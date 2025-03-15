# --- Imports ---#
from PIL import Image
import os
import logging
import platform
import ctypes

# --- other shit here --- #

# --- Functions for Main --- #

def validate_and_preprocess_image(image_path: str) -> str :
    # validates image, resizes or converts the image if necessary, 
    # returns the path to the processed image

    try :
        # open image w/Pillow
        with Image.open(image_path) as img :
            width, height = img.size
            logging.info(f"Original image size: {width}x{height}")

            # get screen res
            screen_width, screen_height = get_screen_resolution()
            logging.info(f"Screen resolution: {screen_width}x{screen_height}")

            # crop image (if) larger than the screen resolution
            if width > screen_width or height > screen_height:
                logging.info("Image is larger than screen resolution. Cropping...")
                
                # calculate cropping box dimensions
                left = (width - screen_width) // 2
                upper = (height - screen_height) // 2
                right = left + screen_width
                lower = upper + screen_height
                
                # crop the image
                img = img.crop((left, upper, right, lower))
                logging.info(f"Cropped image to {screen_width}x{screen_height}.")

            # convert image to compatible format (BMP for Windows) ?
            processed_path = os.path.splitext(image_path)[0] + "_processed.bmp"
            img.save(processed_path, format="BMP")
            logging.info(f"Processed image saved to: {processed_path}")

            return processed_path

    except Exception as e :
        logging.error(f"Error validating or preprocessing image: {e}")
        return ""
    
def get_screen_resolution() -> tuple :
    # returns the screen resolution as (width, height)
    # triple check mac functionality

    try:
        os_name = platform.system()

        if os_name == "Windows" :
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            width = user32.GetSystemMetrics(0)
            height = user32.GetSystemMetrics(1)
            return width, height
        
        elif os_name == "Darwin" :
            # macOS: Use AppKit to get screen resolution
            screen = NSScreen.mainScreen()
            frame = screen.frame()
            width = int(frame.size.width)
            height = int(frame.size.height)
            return width, height
        
        else :
            logging.warning("Screen resolution detection not supported for this OS.")
            return 1920, 1080  # default resolution
        
    except Exception as e :
        logging.error(f"Error getting screen resolution: {e}")
        return 1920, 1080
