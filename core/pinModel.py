# --- Imports ---#
import logging

# --- Models ---#
class Pin :
    def __init__(self, image_url : str) :
        self.image_url = image_url

    def __repr__(self):
        return f"Pin(image_url={self.image_url})"

class Board :
    def __init__(self, name: str, url: str) :
        self.name = name
        self.url = url
        self.pins = []

    def add_pin(self, pin: Pin):
        self.pins.append(pin)
        logging.info(f"Added Pin to Board '{self.name}': {pin}")
    
    def __repr__(self):
        return f"Board(name={self.name}, url={self.url}, pins={len(self.pins)})"

# --- other shit here --- #