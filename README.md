# Pinterest-Wallpaper-Project

## Setup Instructions

### Mac Setup
1. download python3 [https://www.python.org/ftp/python/3.13.2/python-3.13.2-macos11.pkg]
2. download homebrew by opening terminal and entering `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`  
`brew --version` to validate download
3. download git by opening terminal and entering `brew install git`  
`git --version` to validate download
4. download dos2unix by opening terminal and entering `brew install dos2unix`
5. clone the repo & cd into repo
6. in terminal enter `dos2unix setup.sh`
7. in terminal enter `chmod +x setup.sh`
8. in terminal enter `./setup.sh`
9. in terminal enter `source venv/Scripts/activate`

### Windows Setup
1. x  
2. right click on project directory and select 'Open Git Bash here'
3. execute setup script via `./setup.sh`
4. `source venv/Scripts/activate` to activate virutal environment , prompt should show (venv)
5. run script `python main.py`
