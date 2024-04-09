# Environment Setup

## Before installation of ZANSIN

You should check IP addresses of both machines. They are used to connect from ZANSIN Controll Server to ZANSIN Training Machine directory, so they don't have to global IP addresses.

## Log in as zansin at zansin control server

First, log in to the zansin control server as the `zansin` user.
After logging in, ensure you are in the zansin user's home directory.

## Download the Setup Script

Second, download the `zansin.sh` script from the repository:

```bash
wget https://raw.githubusercontent.com/ZANSIN-sec/ZANSIN/main/zansin.sh
```
This script will handle the environment setup process.

## Run the Setup Script
Once the script is downloaded, make it executable and run it with sudo:

```bash
chmod +x zansin.sh
sudo ./zansin.sh
```
