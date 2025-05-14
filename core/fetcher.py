# --- Imports ---#
import time
import logging
import re
from bs4 import BeautifulSoup
from core.pinModel import Board, Pin  # Import the Board and Pin classes
from config import SCROLL_LIMIT, SLEEP_TIME, TEMP_FOLDER
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# --- Excluded URLs ---#
EXCLUDED_URLS = { # annoying ass unrelated pinterest ads (update ?)
    "https://www.pinterest.com/ideas/aesthetic-art/902231121155/",
    "https://www.pinterest.com/ideas/art-inspiration/919907729911/",
    "https://www.pinterest.com/ideas/art/961238559656/",
    "https://www.pinterest.com/ideas/art-reference/893595937733/",
    "https://www.pinterest.com/ideas/cool-art/936897843520/"
}

# --- other shit here --- #

# --- Helper Functions --- #
def get_pin_count_element(driver) -> WebDriverWait : 
    # try multiple strategies for retrieving pin count element
    strategies = [
        (By.XPATH, "//div[contains(text(), 'Pins') and contains(text(), 'Created')]"),
        (By.XPATH, "//div[contains(., 'Pins') and contains(., 'crées')]"),
        (By.CSS_SELECTOR, "div[data-test-id='pin-count']"),
        (By.XPATH, "//div[contains(@class, 'PinCount')]")
    ]

    for strategy in strategies :
        try :
            element = WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located(strategy)
            )
            logging.info(f"Found pin count using {strategy[0]} strategy")
            return element
        except TimeoutException :
            continue
    
    raise NoSuchElementException("Could not find pin count element using any strategy")

def parse_pin_count(text: str) -> int :
    # convert pin count text to integer
    try :
        clean_text = re.sub(r"[^\d,.]", "", text.split()[0])
        if 'k' in clean_text.lower() :
            # Fixed line: Added closing parenthesis for int()
            return int(float(clean_text.lower().replace('k', '')) * 1000)
        return int(clean_text.replace(",", ""))
    except (ValueError, IndexError) as e :
        logging.error(f"Failed to parse pin count from '{text}': {e}")
        raise

def optimized_scroll(driver, increment: int) : 
    # more reliable scrolling w/ loading detection
    driver.execute_script(f"""
        window.scrollTo({{
            top: window.scrollY + {increment},
            behavior: 'smooth'
        }});
    """) # wait time here ?
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'pinimg.com')]"))
    )

def smart_wait(driver) :
    # wait for critical page elements
    try :
        WebDriverWait(driver, 5).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except TimeoutException :
        logging.warning("Page load timed out but proceeding anyway")

# --- Main Function --- #
def fetch_pinterest_data(board_url: str) -> Board :
    driver = None  # Initialize driver for cleanup
    try :
        # --- Browser Setup --- #
        options = Options()
        options.add_argument("--headless")  # toggles physical popup !
        options.add_argument("--force-device-scale-factor=0.8")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("--window-size=2000,1000")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        logging.info("Initializing browser instance...")
        driver = webdriver.Chrome(options=options)
        driver.get(board_url)
        smart_wait(driver)

        # --- Pin Count Extraction --- #
        logging.info("Fetching total pin count...")
        try :
            pin_count_element = get_pin_count_element(driver)
    
            # ensure pin count text exists before screenshot
            pin_count_text = pin_count_element.text.strip()
    
            # create temp folder if needed (validate)
            TEMP_FOLDER.mkdir(parents=True, exist_ok=True)
    
            # save debug screenshot w/ path validation (debugging)
            debug_path = TEMP_FOLDER / "pin_count_debug.png"
            driver.save_screenshot(str(debug_path.resolve()))  # Explicit path conversion
            logging.debug(f"Saved debug screenshot to {debug_path}")
    
            total_pins = parse_pin_count(pin_count_text)
            logging.info(f"Validated total pins: {total_pins}")
        except Exception as e :
            logging.error(f"Critical pin count error: {str(e)}", exc_info=True)
            logging.error(f"Page source snippet:\n{driver.page_source[:1500]}")
            raise
        
        # --- Board Initialization --- #
        board_name = board_url.split("/")[-2]
        board = Board(name=board_name, url=board_url)
        seen_urls = set()
        scroll_attempts = 0
        MAX_ATTEMPTS = 3
        
        # --- Pin Collection Loop --- #
        while len(board.pins) < total_pins and scroll_attempts < SCROLL_LIMIT :
            logging.info(f"Progress: {len(board.pins)}/{total_pins} pins collected")
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            new_pins = 0
            
            for img in soup.find_all("img") :
                img_url = img.get("src")
                if img_url and img_url.startswith("https://i.pinimg.com/") \
                    and img_url not in seen_urls \
                    and img_url not in EXCLUDED_URLS :
                    
                    board.add_pin(Pin(image_url=img_url))
                    seen_urls.add(img_url)
                    new_pins += 1

                    if len(board.pins) >= total_pins :
                        logging.info(f"Target pin count reached: {total_pins}")
                        return board  # exit early

            if new_pins > 0 :
                scroll_attempts = 0
                logging.info(f"Added {new_pins} new pins")
            else :
                scroll_attempts += 1
                logging.warning(f"No new pins (attempt {scroll_attempts}/{MAX_ATTEMPTS})")
                if scroll_attempts >= MAX_ATTEMPTS :
                    break

            optimized_scroll(driver, 1500)
            time.sleep(SLEEP_TIME)

        return board

    # --- Outer Exception Handling --- #
    except Exception as e :
        logging.error(f"Fatal error during fetch: {str(e)}", exc_info=True)
        return Board(name="Error Board", url=board_url)
    
    # --- Mandatory Cleanup --- #
    finally :
        if driver :
            driver.quit()
            logging.info("Browser instance closed")
        # automatic cleanup via cleanup.py will handle the temp folder
