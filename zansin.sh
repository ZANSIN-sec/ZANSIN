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
git clone -b fix/zansin_command https://github.com/zansin-sec/zansin.git &>/dev/null
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
deploy_status "Enter new password for zansin user..." $CYAN
sudo echo "Please enter zansin user's new password:"
read -s new_password
sudo echo "zansin:$new_password" | sudo chpasswd &>/dev/null
sudo sed -i "s/ansible_ssh_pass:.*/ansible_ssh_pass: $new_password/" game-servers.yml &>/dev/null
sudo sed -i "s/ansible_become_password:.*/ansible_become_password: $new_password/" game-servers.yml &>/dev/null

# Log in to training server using SSH password and change password
deploy_status "Changing password on training server..." $YELLOW
sshpass -p "Passw0rd!" ssh -o StrictHostKeyChecking=no zansin@$training_ip &>/dev/null << EOF
sudo echo "zansin:$new_password" | sudo chpasswd
EOF

# Run Ansible playbook
deploy_status "Running Ansible playbook to set up servers..." $GREEN
ansible-playbook -i inventory.ini game-servers.yml

deploy_status "ZANSIN environment setup complete!" $GREEN

sshpass -p "Passw0rd!23" ssh -o StrictHostKeyChecking=no "vendor@$training_ip" << EOF
  cd /home/vendor/game-api
  docker-compose up -d
EOF

deploy_status "ZANSIN services setup complete!" $GREEN

# Stop displaying ZANSIN
kill $ZANSIN_PID
