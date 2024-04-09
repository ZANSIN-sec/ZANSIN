# Repository Requirements

## 2 Ubuntu Linux machines

- Ubuntu 20.04 Server or higher
- Platform doesn't matter (physical environment, virtual environment, public cloud). However, considering you may need to perform exercises multiple times, using VirtualBox which allows creating snapshots is preferable.
- Two Linux machines must be able to communicate with each other and be able to connect via SSH with password authentication.
- Two Linux machines must have access to the Internet.
- A user account named `zansin` with `sudo` privileges on both machines are required, and theirs passwords must be the same.
- Recommended specs: 2GB+ RAM and 1+ CPUs.

> [!NOTE]
> When deploying a ZANSIN environment in a public cloud, it is strongly recommended to limit the source IP address in firewall inbound rules or expose only SSH. Otherwise, vulnerable servers will be exposed on the Internet.
## Setting up Linux (Example)

This example assumes you are installing Ubuntu Server 22.04.4 LTS on VirtualBox.

- Install 2 instances of Ubuntu Linux using the Ubuntu Server 22.04.4 LTS image.
  - Select `Ubuntu Server` as the Install type.
  - During user creation, set the username to `zansin` and the same password on both machines.
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

The user account `zansin` should be pre-created with sudo privileges. If the user account does not exist, you can create it by running the following commands:

```bash
sudo useradd zansin
sudo usermod -aG sudo zansin
echo "zansin:YOUR_PASSWORD" | sudo chpasswd
```

> [!NOTE]
> It is not recommended to publicly disclose passwords. In this repository, the password is provided for illustrative purposes only. In an actual system, you should use a more secure password and keep it private.

