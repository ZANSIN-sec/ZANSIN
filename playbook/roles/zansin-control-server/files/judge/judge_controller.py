#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cmd
# python3 -m venv venv
# .\venv\Scripts\activate.bat
# pip3 install -r requirements.txt
# for vscode: View->Command Palette->set `Python: Select Interpreter`
# Logo: ANSI Shadow at https://manytools.org/hacker-tools/ascii-banner/
import os
import sys
import time
from .util import Utility
from .judge_sql import DbControl
from .modules.checkban import CheckBan
from .modules.checklogin import CheckLogin
from .modules.checkplayer import CheckPlayerInfo
from .modules.checkimageupload import CheckImageUpload
from .modules.checkloginsqli import CheckLoginSQLi
from .modules.checkgacha import CheckGacha
from .modules.checkdocker import CheckDocker
from .modules.checkdebug import CheckDebug
from .modules.checknewuser import CheckNewUser
from .modules.checkwebshell import CheckWebShell
from .modules.checkbattle import CheckBattle
from .modules.checknewusersqli import CheckNewUserSQLi
from .modules.checkssh import CheckSSH
from .modules.checkrecovery import CheckRecovery

OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


def show_banner(utility):
    banner = """
███████╗ █████╗ ███╗   ██╗███████╗██╗███╗   ██╗ █████╗ ██████╗ ██████╗            ██╗██╗   ██╗██████╗  ██████╗ ███████╗
╚══███╔╝██╔══██╗████╗  ██║██╔════╝██║████╗  ██║██╔══██╗██╔══██╗██╔══██╗██╗██╗     ██║██║   ██║██╔══██╗██╔════╝ ██╔════╝
  ███╔╝ ███████║██╔██╗ ██║███████╗██║██╔██╗ ██║███████║██████╔╝██████╔╝╚═╝╚═╝     ██║██║   ██║██║  ██║██║  ███╗█████╗  
 ███╔╝  ██╔══██║██║╚██╗██║╚════██║██║██║╚██╗██║██╔══██║██╔═══╝ ██╔═══╝ ██╗██╗██   ██║██║   ██║██║  ██║██║   ██║██╔══╝  
███████╗██║  ██║██║ ╚████║███████║██║██║ ╚████║██║  ██║██║     ██║     ╚═╝╚═╝╚█████╔╝╚██████╔╝██████╔╝╚██████╔╝███████╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝            ╚════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
""" + 'by ' + os.path.basename(__file__)
    #print(banner)
    utility.print_message(NONE, banner)
    show_credit(utility)
    time.sleep(utility.banner_delay)


# Show credit.
def show_credit(utility):
    credit = u"""
       =[ Version : ZANSINAPP::JUDGE v0.0.1                  ]=
    """
    utility.print_message(NONE, credit)


# Get judge result of attack.
def get_judge_attack_result():
    utility = Utility()
    utility.sql = DbControl(utility)
    return utility.get_technical_point()


OK_BLUE = '\033[94m'      # [*]
NOTE_GREEN = '\033[92m'   # [+]
FAIL_RED = '\033[91m'     # [-]
WARN_YELLOW = '\033[93m'  # [!]
ENDC = '\033[0m'

FLAG_CHECK_LOGIN       = True
FLAG_CHECK_BAN         = True
FLAG_CHECK_PLAYERINFO  = True
FLAG_CHECK_IMAGEUPLOAD = True
FLAG_CHECK_LOGINSQLI   = True
FLAG_CHECK_GACHA       = True
FLAG_CHECK_DOCKER      = True
FLAG_CHECK_DEBUG       = True
FLAG_CHECK_NEWUSER     = True
FLAG_CHECK_WEBSHELL    = True
FLAG_CHECK_BATTLE      = True
FLAG_CHECK_NEWUSERSQLI = True
FLAG_CHECK_SSH         = True
FLAG_CHECK_RECOVERY    = False


# Judge technical points against attack.
def judge_execution_attack(target_host_ip):
    score = 0.0
    debug = False

    target = target_host_ip

    utility = Utility(target)
    show_banner(utility)

    # Initialize Database.
    sql = DbControl(utility)
    utility.sql = sql

    #===========================================================================
    # Ensure check the Login function
    #===========================================================================
    if FLAG_CHECK_LOGIN == True:
        checklogin = CheckLogin(utility, target, "/create/", debug)
        if debug:
            utility.print_message(utility.none, checklogin.__str__())

        json_data = checklogin.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, 'CheckLogin OK(target: %s, description: %s)' % (target, json_data["description"]))
        else:
            utility.print_message(utility.fail, 'CheckLogin NG(target: %s, description: %s)' % (target, json_data["description"]))
            utility.print_message(utility.fail, 'The Web Application is not working currently.')
            utility.print_message(utility.none, '=====================')
            utility.print_message(utility.none, 'Score: 0')
            utility.print_message(utility.none, '=====================')
            exit()
    
        user_id = json_data["user_id"]
        password = json_data["password"]
        session_id = json_data["session_id"]

    #===========================================================================
    # Ensure check BAN function of the web application
    #===========================================================================
    if FLAG_CHECK_BAN == True:
        checkban = CheckBan(utility, target, "/user_list/", debug)
        if debug:
            utility.print_message(utility.none, checkban.__str__())

        json_data = checkban.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, OK_BLUE + 'CheckBan OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
            score += json_data["point"]
        else:
            utility.print_message(utility.fail, FAIL_RED + 'CheckBan NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)

    #===========================================================================
    # Ensure check Player Information Vulnerability
    #===========================================================================
    if FLAG_CHECK_PLAYERINFO == True:
        checkplayer = CheckPlayerInfo(utility, target, "/player/", debug)
        if debug:
            utility.print_message(utility.none, checkplayer.__str__())

        json_data = checkplayer.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, OK_BLUE + 'CheckPlayerInfo OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"] + ENDC))
            score += json_data["point"]
        else:
            utility.print_message(utility.fail, FAIL_RED + 'CheckPlayerInfo NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)

    #===========================================================================
    # Check Image Upload
    #===========================================================================
    if FLAG_CHECK_IMAGEUPLOAD == True:
        checkimageupload = CheckImageUpload(utility, target, "/upload/", debug)
        if debug:
            utility.print_message(utility.none, checkimageupload.__str__())

        json_data = checkimageupload.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, OK_BLUE + 'CheckImageUpload OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
            score += json_data["point"]
        else:
            utility.print_message(utility.fail, FAIL_RED + 'CheckImageUpload NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)

    #===========================================================================
    # Ensure check SQL Injection at Login function
    #===========================================================================
    if FLAG_CHECK_LOGINSQLI == True:
        checkloginsqli = CheckLoginSQLi(utility, target, "/login/", debug)
        if debug:
            utility.print_message(utility.none, checkloginsqli.__str__())

        json_data = checkloginsqli.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, OK_BLUE + 'CheckLoginSQLi OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
            score += json_data["point"]
        else:
            utility.print_message(utility.fail, FAIL_RED + 'CheckLoginSQLi NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)

    #===========================================================================
    # Ensure check SQL Injection at Create User function
    #===========================================================================
    if FLAG_CHECK_NEWUSERSQLI == True:
        checknewusersqli = CheckNewUserSQLi(utility, target, "/create/", debug)
        if debug:
            utility.print_message(utility.none, checknewusersqli.__str__())

        json_data = checknewusersqli.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, OK_BLUE + 'CheckNewUserSQLi OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
            score += json_data["point"]
        else:
            utility.print_message(utility.fail, FAIL_RED + 'CheckNewUserSQLi NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)

    #===========================================================================
    # Ensure check cheat at Gacha function
    #===========================================================================
    if FLAG_CHECK_GACHA == True:
        checkgacha = CheckGacha(utility, target, "/gacha/", debug)
        if debug:
            utility.print_message(utility.none, checkgacha.__str__())

        json_data = checkgacha.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, OK_BLUE + 'CheckGacha OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
            score += json_data["point"]
        else:
            utility.print_message(utility.fail, FAIL_RED + 'CheckGacha NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)

    #===========================================================================
    # Ensure check cheat at Recovery function
    #===========================================================================
    if FLAG_CHECK_RECOVERY == True:
        checkrecovery = CheckRecovery(utility, target, "/recovery/", debug)
        if debug:
            utility.print_message(utility.none, checkrecovery.__str__())

        json_data = checkrecovery.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, OK_BLUE + 'CheckRecovery OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
            score += json_data["point"]
        else:
            utility.print_message(utility.fail, FAIL_RED + 'CheckRecovery NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)

    #===========================================================================
    # Ensure check the port of Docker API is currently open
    #===========================================================================
    if FLAG_CHECK_DOCKER == True:
        checkdocker = CheckDocker(utility, target, "/version", debug)
        if debug:
            utility.print_message(utility.none, checkdocker.__str__())

        json_data = checkdocker.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, OK_BLUE + 'CheckDocker OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
            score += json_data["point"]
        else:
            utility.print_message(utility.fail, FAIL_RED + 'CheckDocker NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)

    #===========================================================================
    # Ensure check the port of Debug API is currently open
    #===========================================================================
    if FLAG_CHECK_DEBUG == True:
        checkdebug = CheckDebug(utility, target, "/debug", debug)
        if debug:
            utility.print_message(utility.none, checkdebug.__str__())

        json_data = checkdebug.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, OK_BLUE + 'CheckDebug OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
            score += json_data["point"]
        else:
            utility.print_message(utility.fail, FAIL_RED + 'CheckDebug NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)


    """
    #===========================================================================
    # Ensure check the port of new_user.php is found currently
    #===========================================================================
    checknewuser = CheckNewUser(target, "/images/players/new_user.php", debug)
    if debug:
        utility.print_message(utility.none, checknewuser.__str__())

    json_data = checknewuser.test()
    if json_data["result"] == True:
        utility.print_message(utility.ok, OK_BLUE + 'CheckNewUser OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
        score += json_data["point"]
    else:
        utility.print_message(utility.fail, FAIL_RED + 'CheckNewUser NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)


    #===========================================================================
    # Ensure check the port of login.php is found currently
    #===========================================================================
    checkwebshell = CheckWebShell(utility, target, "/images/players/login.php", debug)
    if debug:
        utility.print_message(utility.none, checkwebshell.__str__())

    json_data = checkwebshell.test()
    if json_data["result"] == True:
        utility.print_message(utility.ok, OK_BLUE + 'CheckWebShell OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
        score += json_data["point"]
    else:
        utility.print_message(utility.fail, FAIL_RED + 'CheckWebShell NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
    """

    #===========================================================================
    # Ensure check the BattleAPI is working currently
    #===========================================================================
    if FLAG_CHECK_BATTLE == True:
        checkbattle = CheckBattle(utility, target, "/battle/", debug)
        if debug:
            utility.print_message(utility.none, checkbattle.__str__())

        json_data = checkbattle.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, OK_BLUE + 'CheckBattle OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
            score += json_data["point"]
        else:
            utility.print_message(utility.fail, FAIL_RED + 'CheckBattle NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)

    #===========================================================================
    # Ensure change the password of the user
    #===========================================================================
    if FLAG_CHECK_SSH == True:
        checkssh = CheckSSH(utility, target, debug)
        if debug:
            utility.print_message(utility.none, checkssh.__str__())

        json_data = checkssh.test()
        if json_data["result"] == True:
            utility.print_message(utility.ok, OK_BLUE + 'CheckSSH OK(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)
            score += json_data["point"]
        else:
            utility.print_message(utility.fail, FAIL_RED + 'CheckSSH NG(target: %s, score: %f, description: %s)' % (target, json_data["point"], json_data["description"]) + ENDC)

    # Insert technical point to judge db.
    utility.insert_attack_judge_result_to_db(score / utility.point_max * 100)
