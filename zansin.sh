sudo apt update && sudo apt install ansible sshpass
git clone https://github.com/zansin-sec/zansin.git
cd zansin/playbook
# Prompt the user to enter a new IP address
echo "Please enter a new IP address for the training server:"
read training_ip

echo "Please enter a new IP address for the control server:"
read control_ip

# Validate that the input is a valid IP address
if [[ $training_ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] && [[ $control_ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    # Use the sed command to replace the IP address on the specified line with the new IP address
    sed -i '' "2s/.*/$training_ip/" inventory.ini
    sed -i '' "4s/.*/$control_ip/" inventory.ini
else
    echo "Please enter a valid IP address"
fi
echo "IP address were changed successfully!"

# Prompt the user to enter a new password
sudo echo "Please enter zansin user's new password:"
sudo read new_password

sudo echo "zansin:$new_password" | sudo chpasswd
sudo sed -i "s/ansible_ssh_pass:.*/ansible_ssh_pass: $new_password/" game_servers.yml
sudo sed -i "s/ansible_become_password:.*/ansible_become_password: $new_password/" game_servers.yml

# Use sshpass to login with the specified password
sshpass -p "Passw0rd!" ssh -o StrictHostKeyChecking=no zansin@$training_ip << EOF
# Change the password
sudo echo "zansin:$new_password" | sudo chpasswd
EOF

# Run the Ansible playbook to game the servers
ansible-playbook -i inventory.ini game_servers.yml



# # 色定義
# RED="\033[31m"
# GREEN="\033[32m"
# YELLOW="\033[33m"
# BLUE="\033[34m"
# MAGENTA="\033[35m"
# CYAN="\033[36m"
# RESET="\033[0m"

# # ZANSIN を大きく表示する関数（色を引数で受け取るように変更）
# print_zansin() {
#     local color=$1
#     echo -e "${color}"
#     echo "███████╗  █████╗  ███╗   ██╗ ███████╗ ██╗ ███╗   ██╗██╗"
#     echo "╚══███╔╝ ██╔══██╗ ████╗  ██║ ██╔════╝ ██║ ████╗  ██║██║"
#     echo "  ███╔╝  ███████║ ██╔██╗ ██║ ███████╗ ██║ ██╔██╗ ██║██║"
#     echo " ███╔╝   ██╔══██║ ██║╚██╗██║ ╚════██║ ██║ ██║╚██╗██║╚═╝"
#     echo "███████╗ ██║  ██║ ██║ ╚████║ ███████║ ██║ ██║ ╚████║██╗"
#     echo "╚══════╝ ╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚══════╝ ╚═╝ ╚═╝  ╚═══╝╚═╝"
#     echo -e "${RESET}"
# }

# # 進捗表示関数
# deploy_status() {
#     local message=$1
#     local color=$2
#     echo -e "${color}${message}${RESET}"
# }

# # メイン処理
# clear
# print_zansin $CYAN
# deploy_status "Deploying ZANSIN Control Server..." $YELLOW
# sleep 2 # 進捗のシミュレーション

# deploy_status "ZANSIN Control Server Deployed!" $GREEN
# sleep 2 # 進捗のシミュレーション

# deploy_status "Deploying Training Machine..." $YELLOW
# sleep 2 # 進捗のシミュレーション

# deploy_status "Training Machine Deployed!" $GREEN
# sleep 2 # 最終状態を見せる

# # ZANSINの表示を停止する
# kill $ZANSIN_PID
