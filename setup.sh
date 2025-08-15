#!/bin/bash
# setup.sh
# Cross Platform setup script for Pinterest Wallpaper Engine

# variables
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"

# check if python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 not installed, try again after installing python"
    exit 1
fi

# create a virtual environment
echo "creating a virtual environment..."
python3 -m venv $VENV_DIR

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source "$VENV_DIR/bin/activate"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source "$VENV_DIR/Scripts/activate"
else
    echo "Unsupported OS. Manual setup required."
    exit 1
fi

# upgrade pip
echo "upgrading pip..."
pip install --upgrade pip

# install dependencies
echo "Installing dependencies..."
pip install -r "$REQUIREMENTS_FILE"

# macOS-specific driver setup
echo "Configuring WebDriver..."
webdriver-manager install --drivers chrome

# Make chromedriver executable (macOS/Linux)
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Setting ChromeDriver permissions..."
    find "$VENV_DIR" -name 'chromedriver' -exec chmod +x {} \;
fi

# macOS-specific setup
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installing macOS dependencies..."
    pip install pyobjc-core==11.0 pyobjc==11.0 appscript==1.2.2
    
    echo "Configuring macOS permissions..."
    # Remove quarantine attributes
    find "$VENV_DIR" -name 'chromedriver' -exec xattr -d com.apple.quarantine {} \;
    
    # Additional macOS fixes
    echo "Applying macOS compatibility fixes..."
    # Fix for Tkinter on macOS
    pip install pillow --upgrade --force-reinstall
fi

# Final instructions
echo -e "\n\033[1;32mSetup complete!\033[0m"
echo "To run the application:"
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "  source $VENV_DIR/bin/activate"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "  source $VENV_DIR/Scripts/activate"
fi
echo "  python main.py"

# additional setup steps here
# ...
