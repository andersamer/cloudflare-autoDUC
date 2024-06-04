#!/bin/bash

DEST="$HOME/.local/bin" # Edit this variable if you want to change the installation directory
INSTALL_DIR="$DEST/cloudflare-autoDUC"

# Function to install dependencies
install_dependencies() {
    echo "Installing required dependencies..."
    sudo apt-get update
    sudo apt-get install -y python3-pip   # Install pip for Python 3
    pip3 install -r requirements.txt      # Install Python dependencies from requirements.txt
}

# Function to install the Python script
install_python_script() {
    echo "Installing Python script..."
    sudo mkdir "$INSTALL_DIR"                # Make a directory for the script
    sudo cp ./main.py "$INSTALL_DIR"         # Copy the main script
    sudo cp ./autoDUC.py "$INSTALL_DIR"      # Copy the library script
    sudo cp ./conf.json "$INSTALL_DIR"       # Copy the conf script
    sudo touch "$INSTALL_DIR/update.log"     # Make the update.log file
    sudo chmod 666 "$INSTALL_DIR/update.log" # Make the log file readable/writeable
    sudo chmod 666 "$INSTALL_DIR/conf.json"  # Make the .env file readable/writeable
    sudo chmod +x "$INSTALL_DIR/main.py"     # Make script executable
}

# Function to set up cronjob
setup_cronjob() {
    echo "Setting up cronjob..."
    (crontab -l ; echo "*/30 * * * * /usr/bin/python3 $INSTALL_DIR/main.py") | crontab -
}

# Main function
main() {
    install_dependencies
    install_python_script
    setup_cronjob
    echo "Installation completed successfully!"
}

# Run the main function
main
