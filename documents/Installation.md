# Installation

- [Installation](#installation)
  - [Requirements](#requirements)
  - [Linux Installation](#linux-installation)
    - [Creating ZANSIN user](#creating-zansin-user)
    - [Installing OpenSSH](#installing-openssh)
  - [ZANSIN Deploymentation](#zansin-deploymentation)

## Requirements

- **Ubuntu 20.04** Server or higher
- Platform doesn't matter (physical environment, virtual environment, public cloud). 
  - However, considering you may need to perform exercises multiple times, using **VirtualBox** which allows creating snapshots is preferable.
- Two Linux machines must be able to **communicate with each other** and be able to connect via **SSH with password authentication**. 
  - In the initial state of starting the exercise, please ensure that there are **no communication restrictions** between the two Linux hosts.
- Two Linux machines must have **access to the Internet**.
- A user account named **`zansin` with `sudo`** privileges on both machines are required, and **theirs passwords must be the same**.
- Recommended system requirements: 2GB+ RAM and 1+ CPUs per Linux host.

> [!Caution]
> When deploying a ZANSIN environment in a public cloud, it is strongly recommended to limit the source IP address in firewall inbound rules or expose only SSH. Otherwise, vulnerable servers will be exposed on the Internet.


## Linux Installation

The example below assumes that you are installing Ubuntu Server 22.04.4 LTS on VirtualBox. 
Since ZANSIN requires two Linux hosts, you will need to repeat this installation process twice.

1. During the Ubuntu installation process, please configure the following settings:
   - Choose `Ubuntu Server` as the installation type.
   - When creating a user, set the username to `zansin` and use the same password for both machines.
   - In the SSH Setup screen, check the `Install OpenSSH Server`.
2. After the installation, to enable easy connectivity between the virtual machines and internet access, use the "Bridged Adapter" for the Network Adapter setting.

If you were unable to create the user 'zansin' or install OpenSSH during the Ubuntu installation process, execute the following commands after logging into Ubuntu.

### Creating ZANSIN user

```bash
sudo useradd zansin
sudo usermod -aG sudo zansin
echo "zansin:YOUR_PASSWORD" | sudo chpasswd
```

### Installing OpenSSH

```bash
sudo apt update
sudo apt install openssh-server
```

## ZANSIN Deploymentation

Prior to installing ZANSIN, you should verify the IP addresses of both machines.

> [!Note]
> These addresses are utilized for connecting from the ZANSIN Control Server to the ZANSIN Training Machine directory, so they do not necessarily need to be global IP addresses.

1. Log in to the ZANSIN Control Server using the `zansin` user.

2. GDownload `zansin.sh` from the GitHub repository:

    ```bash
    wget https://raw.githubusercontent.com/ZANSIN-sec/ZANSIN/main/zansin.sh
    ```

3. Give executable permission to `zansin.sh` and execute it:
    ```bash
    chmod +x zansin.sh
    sudo ./zansin.sh
    ```
