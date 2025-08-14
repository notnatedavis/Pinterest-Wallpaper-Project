#!/bin/bash
# setup.sh
# Should handle cross platform setup

# variables
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"

# check if python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 not installed, try again after installing python"
    exit 1
fi

# create a virtual environment
echo "creating a virtual environment . . ."
python3 -m venv $VENV_DIR

# activate virtual environment (macOS & Windows compatible)
echo "activating virtual environment . . ."
source $VENV_DIR/bin/activate

# upgrade pip
echo "upgrading pip . . ."
pip install --upgrade pip

# install dependencies
echo "Installing dependencies..."
pip install -r "$REQUIREMENTS_FILE"

# macOS-specific driver setup
echo "Configuring WebDriver for macOS..."
webdriver-manager install --drivers chrome

# fix permissions for ChromeDriver
find "$VENV_DIR" -name 'chromedriver' -exec chmod +x {} \;

# additional setup steps here
# ...
