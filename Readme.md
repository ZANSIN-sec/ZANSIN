![ZANSIN](./images/F317526F1119930E21EC0A70B21E8A0F892AF67B.png)

ZANSIN
=================

![Ansible](https://img.shields.io/badge/-Ansible-EE0000.svg?logo=ansible&style=flat")

ZANSIN is envisioned as a GROUNDBREAKING cybersecurity training tool designed to equip users against the ever-escalating complexity of cyber threats. It achieves this by providing learners with a platform to engage in simulated cyberattack scenarios, supervised and designed by experienced pentesters.
This comprehensive approach allows learners to actively apply security measures, perform system modifications, and handle incident responses to counteract the attacks. Engaging in this hands-on practice within realistic environments enhances their server security skills and provides practical experience in identifying and mitigating cybersecurity risks. ZANSIN's flexible design accommodates diverse skill levels and learning styles, making it a comprehensive and evolving platform for cybersecurity education.

## What does 'ZANSIN' mean?

- [What does 'ZANSIN' mean?](./documents/ZANSIN.md)

## System Overview

- [System Overview](./documents/SystemOverview.md)
 
## Deploymentation

- [Requirements](./documents/Requirements.md)
- [Deploymentation](./documents/Deploymentation.md)

## Play Scenario

```bash
sudo useradd zansin
sudo usermod -aG sudo zansin
echo "zansin:Passw0rd!" | sudo chpasswd
sudo apt install ansible
```

<!-- ### SSH Key Pair Generation

And, create a pair of private and public keys in /home/hardmini/.ssh/, and name the private key `team.pem` and the public key `team.pub`.

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/team
mv ~/.ssh/team ~/.ssh/team.pem
```

Copy the Public Key to Your Remote Server:

Use the ssh-copy-id command to add your public key (team.pub) to the authorized_keys
file of the hardmini user on the remote server. Replace your_remote_host with the actual
hostname or IP address of your server.

Example:

```bash
cat ~/.ssh/team.pub | ssh hardmini@your_remote_host 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
``` -->

###  Clone the repository

Be back to local computer and clone the repository and navigate to the playbook directory to execute the Ansible playbook

```bash
git clone https://github.com/zansin-sec/zansin.git
cd zanshin/playbook
```

### Setup Attack Server

```bash
sudo useradd zansin
sudo usermod -aG sudo zansin
echo "zansin:Passw0rd!" | sudo chpasswd
sudo apt install sshpass
```


### Configure Ansible Inventory

Document the IP address or hostname of the Ubuntu 20.04+ host intended for the game environment setup. '
Update the `inventory.ini` file located in the playbook directory, specifically under the [game-servers] section with the host details.

```bash
ansible-playbook -i inventory.ini game-servers.yml
```

## Components

The user connecting must have the permissions to execute sudo, and please enter their password.

```mermaid
  graph LR
    A[Ansible Control Node] -- Ansible connection --> B[game-server]
    A -- Ansible connection --> C[game-server]
    A -- Ansible connection --> D[game-server]
    A -- Ansible connection --> E[red-server]
```
- [Scenario - MINI QUEST](./documents/MINIQUEST.md)
- [Usage](./documents/Usage.md)

## Cite This Work

Details on how to cite ZANSIN in your academic and professional works will be provided after our official release.
