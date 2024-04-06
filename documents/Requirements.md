# Repository Requirements

## 2 Ubuntu Linux machines
- Ubuntu 20.04 Server or higher
- Platform doesn't matter (physical environment, virtual environment, public cloud). However, considering you may need to perform exercises multiple times, using VirtualBox which allows creating snapshots is preferable.
- The 2 Linux machines should be able to connect to each other via SSH.
- The 2 Linux machines should have internet access.
- A user account named `zansin` with `sudo` privileges (Password: `Passw0rd!`).
- Recommended specs: 4GB+ RAM and 2+ CPUs.

## Setting up Linux (Example)

This example assumes you are installing Ubuntu Server 22.04.4 LTS on VirtualBox.

- Install 2 instances of Ubuntu Linux using the Ubuntu Server 22.04.4 LTS image.
    - Select `Ubuntu Server` as the Install type.
    - During user creation, set the username to `zansin` and password to `Passw0rd!23`.
    - In the SSH Setup screen, check `Install OpenSSH Server`.
    - To allow easy connectivity between the virtual machines and internet access, use the `Bridged Adapter` for the Network Adapter setting.

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
