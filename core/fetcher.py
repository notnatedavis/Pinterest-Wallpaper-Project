# --- Imports ---#
import time
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import SCROLL_LIMIT, SLEEP_TIME 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.pinModel import Board, Pin  # Import the Board and Pin classes

# --- Excluded URLs ---#
EXCLUDED_URLS = { # annoying ass unrelated pinterest ads
    "https://www.pinterest.com/ideas/aesthetic-art/902231121155/",
    "https://www.pinterest.com/ideas/art-inspiration/919907729911/",
    "https://www.pinterest.com/ideas/art/961238559656/",
    "https://www.pinterest.com/ideas/art-reference/893595937733/",
    "https://www.pinterest.com/ideas/cool-art/936897843520/"
}

# --- other shit here --- #

# --- Functions for Main --- #

def fetch_pinterest_data(board_url: str) -> Board :
    # fetches image URLs from the given Pinterest board URL and returns a list

    try:
        # set up selenium WebDriver w/Chrome options
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--headless")  # toggles physical popup
        options.add_argument("--force-device-scale-factor=0.5")  # sets zoom out before loading url !OPTIMIZE
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=3000,2000") # predefined window size (w x h) !OPTIMIZE

        logging.info("Launching browser...")
        driver = webdriver.Chrome(options=options)  # ensure `chromedriver` is in PATH or specify its location
        driver.get(board_url)

        time.sleep(0.2) # initial buffer

        # search for total pin count w/ XPath (specific to each url ?) update universally ?
        logging.info("Fetching total pin count...")

        # fetch total pin count
        try:
            pin_count_element = WebDriverWait(driver, 3).until(
                # this works ! (test on other boards)
                EC.presence_of_element_located((By.XPATH, '//*[@id="mweb-unauth-container"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[1]/div/div/span/div/div/div/div[1]'))
            )
            pin_count_text = pin_count_element.text # store this var for later
            total_pins = int(pin_count_text.split()[0])  # Extract the number from the text
            logging.info(f"Total board Pin count : {total_pins}")
        except Exception as e:
            logging.warning(f"Could not determine total pin count: {e}")
            total_pins = None
        
        # Create a Board object
        board_name = board_url.split("/")[-2]  # Extract board name from URL
        board = Board(name=board_name, url=board_url)
        
        scroll_increment = 1000  # Adjustable scroll increment !OPTIMIZE
        pins_collected = 0  # Track the number of pins collected
        seen_urls = set()  # Track URLs we've already processed
        no_new_pins_attempts = 0  # Track how many times no new pins were found (failsafe)
        
        while True:
            # Parse the page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Iterate through each <img> element
            new_pins_added = 0
            for img in soup.find_all("img"):
                image_url = img.get("src")
                if (
                    image_url
                    and image_url.startswith("https://i.pinimg.com/")  # Ensure it's a Pinterest image
                    and image_url not in seen_urls  # Avoid duplicates
                    and image_url not in EXCLUDED_URLS  # Exclude unwanted URLs
                ) :
                    # Add the pin to the board
                    pin = Pin(image_url=image_url)
                    board.add_pin(pin)
                    pins_collected += 1
                    seen_urls.add(image_url)
                    new_pins_added += 1

                    # Log the new pin
                    logging.info(f"Added Pin {pins_collected}: {image_url}")

                    # Stop if we've collected all pins
                    if total_pins is not None and pins_collected >= total_pins:
                        logging.info(f"All {total_pins} pins collected. Stopping fetch.")
                        driver.quit()
                        return board

            logging.info(f"Found {new_pins_added} new valid URLs. Total Pins in Board: {len(board.pins)}")

            # Check if no new pins were found in this iteration
            if new_pins_added == 0:
                no_new_pins_attempts += 1
                if no_new_pins_attempts >= 3:  # Stop if no new pins are found after 3 attempts
                    logging.info("No new pins found after multiple attempts. Stopping fetch.")
                    break
            else:
                no_new_pins_attempts = 0  # Reset the counter if new pins were found

            # Scroll to load more pins
            current_scroll_position = driver.execute_script("return window.scrollY;")
            driver.execute_script(f"window.scrollTo(0, {current_scroll_position + scroll_increment});")
            time.sleep(SLEEP_TIME)  # Wait for new pins to load
            logging.info("Scrolled to load more pins.")

        driver.quit()

        logging.info(f"Finished fetching data. Board '{board.name}' has {len(board.pins)} Pins.")
        return board
    
    except Exception as e :
        logging.error(f"Error fetching Pinterest data: {e}")
        return Board(name="Error Board", url="")  # Return an empty Board in case of error