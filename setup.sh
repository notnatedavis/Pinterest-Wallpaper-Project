#!/bin/bash

# variables
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"

# check if python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 not installed, try again after installing python"
    exit 1
fi

# create a virtual environment for packages
echo "creating a virtual environment . . ."
python3 -m venv $VENV_DIR

# activate virtual environment
echo "activating virtual environment . . ."
source $VENV_DIR/Scripts/activate

# upgrade pip
echo "upgrading pip . . ."
pip install --upgrade pip

# install dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "installing dependencies from $REQUIREMENTS_FILE . . ."
    pip install -r $REQUIREMENTS_FILE
else
    echo "$REQUIREMENTS_FILE not found. No dependencies to install"
fi

# additional setup steps here
# ...
