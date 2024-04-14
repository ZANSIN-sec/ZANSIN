#!/bin/bash

# Color definitions
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
RESET="\033[0m"

# Function to display ZANSIN in large font
print_zansin() {
    local color=$1
    echo -e "${color}"
    echo "███████╗ █████╗ ███╗   ██╗███████╗██╗ ███╗   ██╗██╗"
    echo "╚══███╔╝██╔══██╗████╗  ██║██╔════╝██║ ████╗  ██║██║"
    echo "  ███╔╝ ███████║██╔██╗ ██║███████╗██║ ██╔██╗ ██║██║"
    echo " ███╔╝  ██╔══██║██║╚██╗██║╚════██║██║ ██║╚██╗██║╚═╝"
    echo "███████╗██║  ██║██║ ╚████║███████║██║ ██║ ╚████║██╗"
    echo "╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═╝  ╚═══╝╚═╝"
    echo -e "${RESET}"
}

# Progress display function
deploy_status() {
    local message=$1
    local color=$2
    echo -e "${color}${message}${RESET}"
}

# Main processing
clear
print_zansin $CYAN

# Install packages and clone repository
deploy_status "Installing required packages..." $YELLOW
sudo apt update &>/dev/null && sudo apt install -y ansible sshpass git &>/dev/null
git clone https://github.com/zansin-sec/zansin.git &>/dev/null
cd zansin/playbook &>/dev/null

# Enter IP addresses
deploy_status "Enter new IP addresses..." $CYAN
echo "Please enter a new IP address for the training server:"
read training_ip
echo "Please enter a new IP address for the control server:"
read control_ip

# Validate and replace IP addresses
if [[ $training_ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] && [[ $control_ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    deploy_status "Updating inventory file with new IP addresses..." $GREEN
    sed -i "2s/.*/$training_ip/" inventory.ini &>/dev/null
    sed -i "4s/.*/$control_ip/" inventory.ini &>/dev/null
else
    deploy_status "Invalid IP address. Please try again." $RED
    exit 1
fi

# Enter and set password
deploy_status "Enter current password for zansin user..." $CYAN
sudo echo "Please enter zansin user's current password:"
read -s current_password
sudo sed -i "s/ansible_ssh_pass:.*/ansible_ssh_pass: $current_password/" game-servers.yml &>/dev/null
sudo sed -i "s/ansible_become_password:.*/ansible_become_password: $current_password/" game-servers.yml &>/dev/null

# Run Ansible playbook
deploy_status "Running Ansible playbook to set up servers..." $GREEN
ansible-playbook -i inventory.ini game-servers.yml

deploy_status "ZANSIN environment setup complete!" $GREEN

sshpass -p "Passw0rd!23" ssh -o StrictHostKeyChecking=no "vendor@$training_ip" << EOF
  cd /home/vendor/game-api
  docker-compose up -d
EOF

# Set up Red Controller
# Check if python3 and pip3 are installed, install if not
deploy_status "Checking for Python3 and pip3 for ZANSIN Red Controller..." $YELLOW
RED_CONTROLLER_PYTHON3_INSTALLED=$(command -v python3.10)
RED_CONTROLLER_PIP3_INSTALLED=$(command -v pip3)
if [[ -z "RED_CONTROLLER_PYTHON3_INSTALLED" ]]; then
    deploy_status "Python3 not found. Installing Python3.10 for ZANSIN Red Controller..." $RED
    sudo apt update && sudo apt install -y python3.10 python3.10-venv python3.10-dev
fi
if [[ -z "$RED_CONTROLLER_PIP3_INSTALLED" ]]; then
    deploy_status "pip3 not found. Installing pip3 for ZANSIN Red Controller..." $RED
    sudo apt update && sudo apt install -y python3-pip
fi

# Set virtual environment path for Red Controller
RED_CONTROLLER_VENV_PATH="red_controller_venv"

# Activate "red_controller_venv"
deploy_status "Setting up virtual environment for ZANSIN Red Controller..." $YELLOW
python3.10 -m venv RED_CONTROLLER_VENV_PATH
source $RED_CONTROLLER_VENV_PATH/bin/activate

# Set environment variable for requirements.txt
export RED_CONTROLLER_VENV_PATH_REQUIREMENTS_PATH="playbook/roles/zansin-control-server/files/requirements.txt"

# Install required Python packages from requirements.txt
deploy_status "Installing required Python packages for ZANSIN Red Controller..." $YELLOW
pip3 install -r RED_CONTROLLER_VENV_PATH_REQUIREMENTS_PATH

# Deactivate "red_controller_venv"
deactivate

deploy_status "ZANSIN services setup complete!" $GREEN

# Stop displaying ZANSIN
kill $ZANSIN_PID
