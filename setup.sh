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

# activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source "$VENV_DIR/bin/activate"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source "$VENV_DIR/Scripts/activate"
else
    echo "Unsupported OS. Manual setup required."
    exit 1
fi

# upgrade pip + dependencies
echo "upgrading pip..."
pip install --upgrade pip
pip install -r "$REQUIREMENTS_FILE"

# pre-webdriver macOS SSL fix (update!)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Applying macOS SSL workaround..."
    pip uninstall -y urllib3
    pip install "urllib3==1.26.20" --no-cache-dir
fi

# ChromeDriver installation
echo "Installing ChromeDriver..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # manual installation for macOS
    CHROME_VERSION=$(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version | awk '{print $3}')
    CHROME_MAJOR=$(echo $CHROME_VERSION | cut -d. -f1)
    CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR"
    CHROMEDRIVER_VERSION=$(curl -s "$CHROMEDRIVER_URL")
    
    echo "downloading ChromeDriver $CHROMEDRIVER_VERSION..."
    curl -L "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_mac64.zip" -o chromedriver.zip
    unzip chromedriver.zip
    rm chromedriver.zip
    mv chromedriver "$VENV_DIR/bin/"
    chmod +x "$VENV_DIR/bin/chromedriver"
    xattr -d com.apple.quarantine "$VENV_DIR/bin/chromedriver"
else
    # use webdriver-manager for other platforms
    python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
fi

# macOS Specific Setup
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "installing macOS dependencies..."
    pip install pyobjc-core==11.0 pyobjc==11.0 appscript==1.2.2
    
    echo "fixing macOS image handling..."
    pip install pillow==11.1.0 --upgrade --force-reinstall
    
    echo "final macOS permissions check..."
    find "$VENV_DIR" -name 'chromedriver' -exec xattr -d com.apple.quarantine {} \;
fi

# linux support
if [[ "$OSTYPE" == "linux"* ]]; then
    echo "configuring Linux permissions..."
    find "$VENV_DIR" -name 'chromedriver' -exec chmod +x {} \;
fi

# wrap up
echo -e "setup complete"
echo "run w/: "
echo "   source $VENV_DIR/bin/activate"
echo "   python main.py"

# additional setup steps here
# ...

# testing
echo -e "\n Running test..."
python -c "from selenium import webdriver; from selenium.webdriver.chrome.service import Service; from selenium.webdriver.chrome.options import Options; options = Options(); options.add_argument('--headless'); service = Service(executable_path='$VENV_DIR/bin/chromedriver'); driver = webdriver.Chrome(service=service, options=options); print('Selenium test successful!'); driver.quit()"