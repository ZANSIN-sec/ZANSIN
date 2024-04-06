# Repository Requirements

## Operating System

- Ubuntu 20.04 Server or higher

## Installed Software

- OpenSSH

If OpenSSH is not installed, you can install it by running the following command:

```bash
sudo apt update
sudo apt install openssh-server
```
## User Account
- Username: zansin
- Password: Passw0rd!

A user account with the above username and password should be pre-created with sudo privileges. If the user account does not exist, you can create it by running the following commands:

```bash
sudo useradd zansin
sudo usermod -aG sudo zansin
echo "zansin:Passw0rd!" | sudo chpasswd
```

## Security Notice
It is not recommended to publicly disclose passwords. In this repository, the password is provided for illustrative purposes only. In an actual system, you should use a more secure password and keep it private.
