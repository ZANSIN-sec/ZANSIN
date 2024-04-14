#!/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import random
import codecs
import hashlib
import requests
import urllib.parse
import json
import re
import time
import configparser
import paramiko
from statistics import mean
from urllib3 import util
from datetime import datetime
from logging import getLogger, FileHandler, Formatter
from collections import deque

# Printing colors.
OK_BLUE = '\033[94m'      # [*]
NOTE_GREEN = '\033[92m'   # [+]
FAIL_RED = '\033[91m'     # [-]
WARN_YELLOW = '\033[93m'  # [!]
ENDC = '\033[0m'
PRINT_OK = OK_BLUE + '[*]' + ENDC
PRINT_NOTE = NOTE_GREEN + '[+]' + ENDC
PRINT_FAIL = FAIL_RED + '[-]' + ENDC
PRINT_WARN = WARN_YELLOW + '[!]' + ENDC

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Utility class.
class Utility:
    # def __init__(self, target=None, team_name=None, debug=False):
    def __init__(self, target="", debug=False, sql=None):
        self.target = target
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))

        # Read judge_config.ini.
        full_path = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'judge_config.ini'), encoding='utf-8')

        try:
            # Common
            self.ua = config['Common']['user-agent']
            self.sql = sql
            self.request_schema = config['Common']['request_schema']
            self.banner_delay = float(config['Common']['banner_delay'])
            self.con_timeout = float(config['Common']['con_timeout'])
            self.report_date_format = config['Common']['date_format']
            self.proxy_addr = config['Common']['proxy_addr']
            self.proxy_user = config['Common']['proxy_user']
            self.proxy_pass = config['Common']['proxy_pass']
            self.ok = config['Common']['ok']
            self.note = config['Common']['note']
            self.warning = config['Common']['warning']
            self.fail = config['Common']['fail']
            self.none = config['Common']['none']
            self.loop_wait_time = float(config['Common']['loop_wait_time'])

            # SSH Connect.
            self.ssh_password = config['SSH_Login']['password']
            self.ssh_cmd = config['SSH_Login']['cmd']
            self.ssh_users = (config['SSH_Login']['users']).split('@')
            
            # API: New User.
            self.api_new_user_method = config['API_NewUser']['method']
            self.api_new_user_ctype = config['API_NewUser']['content-type']
            if debug:
                self.api_new_user_url = config['API_NewUser']['url_debug']
            else:
                self.api_new_user_url = config['API_NewUser']['url'].format(self.target)
            self.api_new_user_params = {}
            for param in str(config['API_NewUser']['params']).split('@'):
                self.api_new_user_params[param] = ''
            
            # API: Login.
            self.api_login_method = config['API_Login']['method']
            self.api_login_ctype = config['API_Login']['content-type']
            if debug:
                self.api_login_url = config['API_Login']['url_debug']
            else:
                self.api_login_url = config['API_Login']['url'].format(self.target)
            self.api_login_params = {}
            for param in str(config['API_Login']['params']).split('@'):
                self.api_login_params[param] = ''
            
            # API: Player
            self.api_pinfo_method = config['API_PlayerInfo']['method']
            self.api_pinfo_ctype = config['API_PlayerInfo']['content-type']
            if debug:
                self.api_pinfo_url = config['API_PlayerInfo']['url_debug']
            else:
                self.api_pinfo_url = config['API_PlayerInfo']['url'].format(self.target)
            self.api_pinfo_params = {}
            for param in str(config['API_PlayerInfo']['params']).split('@'):
                self.api_pinfo_params[param] = ''
            
            # API: ImageUpload
            self.api_imgupload_method = config['API_ImageUpload']['method']
            self.api_imgupload_ctype = config['API_ImageUpload']['content-type']
            if debug:
                self.api_imgupload_url = config['API_ImageUpload']['url_debug']
            else:
                self.api_imgupload_url = config['API_ImageUpload']['url'].format(self.target)
            self.api_imgupload_download_url = config['API_ImageUpload']['download_url'].format(self.target)
            self.api_imgupload_params = {}
            for param in str(config['API_ImageUpload']['params']).split('@'):
                self.api_imgupload_params[param] = ''
            
            # API: Gacha
            self.api_gacha_method = config['API_Gacha']['method']
            self.api_gacha_ctype = config['API_Gacha']['content-type']
            if debug:
                self.api_gacha_url = config['API_Gacha']['url_debug']
            else:
                self.api_gacha_url = config['API_Gacha']['url'].format(self.target)
            self.api_gacha_params = {}
            for param in str(config['API_Gacha']['params']).split('@'):
                self.api_gacha_params[param] = ''
            
            # API: Recovery
            self.api_recovery_method = config['API_Recovery']['method']
            self.api_recovery_ctype = config['API_Recovery']['content-type']
            if debug:
                self.api_recovery_url = config['API_Recovery']['url_debug']
            else:
                self.api_recovery_url = config['API_Recovery']['url'].format(self.target)
            self.api_recovery_params = {}
            for param in str(config['API_Recovery']['params']).split('@'):
                self.api_recovery_params[param] = ''
            
            # API: Charge
            self.api_charge_method = config['API_Charge']['method']
            self.api_charge_ctype = config['API_Charge']['content-type']
            if debug:
                self.api_charge_url = config['API_Charge']['url_debug']
            else:
                self.api_charge_url = config['API_Charge']['url'].format(self.target)
            self.api_charge_params = {}
            for param in str(config['API_Charge']['params']).split('@'):
                self.api_charge_params[param] = ''
            
            # API: Docker
            self.api_docker_method = config['API_Docker']['method']
            self.api_docker_ctype = config['API_Docker']['content-type']
            if debug:
                self.api_docker_url = config['API_Docker']['url_debug']
            else:
                self.api_docker_url = config['API_Docker']['url'].format(self.target)
            self.api_docker_params = {}
            for param in str(config['API_Docker']['params']).split('@'):
                self.api_docker_params[param] = ''

            # API: CourseGet
            self.api_courseget_method = config['API_CourseGet']['method']
            self.api_courseget_ctype = config['API_CourseGet']['content-type']
            if debug:
                self.api_courseget_url = config['API_CourseGet']['url_debug']
            else:
                self.api_courseget_url = config['API_CourseGet']['url'].format(self.target)
            self.api_courseget_params = {}
            for param in str(config['API_CourseGet']['params']).split('@'):
                self.api_courseget_params[param] = ''

            # API: CourseSet
            self.api_courseset_method = config['API_CourseSet']['method']
            self.api_courseset_ctype = config['API_CourseSet']['content-type']
            if debug:
                self.api_courseset_url = config['API_CourseSet']['url_debug']
            else:
                self.api_courseset_url = config['API_CourseSet']['url'].format(self.target)
            self.api_courseset_params = {}
            for param in str(config['API_CourseSet']['params']).split('@'):
                self.api_courseset_params[param] = ''

            # API: Battle
            self.api_battle_method = config['API_Battle']['method']
            self.api_battle_ctype = config['API_Battle']['content-type']
            if debug:
                self.api_battle_url = config['API_Battle']['url_debug']
            else:
                self.api_battle_url = config['API_Battle']['url'].format(self.target)
            self.api_battle_params = {}
            for param in str(config['API_Battle']['params']).split('@'):
                self.api_battle_params[param] = ''

            # Page: UserBan
            if debug:
                self.ban_url = config['Check_Ban']['url_debug']
            else:
                self.ban_url = config['Check_Ban']['url'].format(self.target)
            self.ban_keyword = config['Check_Ban']['keyword']

            # Page: Debug1
            if debug:
                self.debug1_url = config['Check_Debug1']['url_debug']
            else:
                self.debug1_url = config['Check_Debug1']['url'].format(self.target)
            self.debug1_keyword = config['Check_Debug1']['keyword']

            # Page: Debug2
            if debug:
                self.debug2_url = config['Check_Debug2']['url_debug']
            else:
                self.debug2_url = config['Check_Debug2']['url'].format(self.target)
            self.debug2_keyword = config['Check_Debug2']['keyword']

            # Page: NewUser
            if debug:
                self.newuser_url = config['Check_NewUser']['url_debug']
            else:
                self.newuser_url = config['Check_NewUser']['url'].format(self.target)
            self.newuser_keyword = config['Check_NewUser']['keyword']

            # Page: WebShell
            if debug:
                self.webshell_url = config['Check_WebShell']['url_debug']
            else:
                self.webshell_url = config['Check_WebShell']['url'].format(self.target)
            self.webshell_keyword = config['Check_WebShell']['keyword']

            # Points
            self.point_userlist = config['Point']['page_user_list']
            self.point_debug1 = config['Point']['page_debug1']
            self.point_debug2 = config['Point']['page_debug2']
            #self.point_websehll = config['Point']['page_webshell']
            #self.point_newuser = config['Point']['page_newuser_cheat']
            self.point_loginsqli = config['Point']['login_sqli']
            self.point_battlecheat = config['Point']['battle_cheat']
            self.point_gachacheat = config['Point']['gacha_cheat']
            #self.point_recoverycheat = config['Point']['recovery_cheat']
            self.point_dockerapi = config['Point']['dockerapi_vuln']
            self.point_playerinfo = config['Point']['playerinfo_vuln']
            self.point_imageupload = config['Point']['imgupload_vuln']
            self.point_createusersqli = config['Point']['createuser_sqli']
            self.point_loginssh = config['Point']['login_ssh']
            #self.point_max = float(self.point_userlist) + float(self.point_debug1) + float(self.point_debug2) + float(self.point_websehll) + float(self.point_newuser) + float(self.point_recoverycheat) \
            self.point_max = float(self.point_userlist) + float(self.point_debug1) + float(self.point_debug2) \
                + float(self.point_loginsqli) + float(self.point_battlecheat) + float(self.point_gachacheat) + float(self.point_dockerapi) + float(self.point_playerinfo) \
                    + float(self.point_imageupload) + float(self.point_createusersqli) \
                    + float(self.point_loginssh)
            
        except Exception as e:
            self.print_message(FAIL, 'Reading judge_config.ini is failure : {}'.format(e))
            sys.exit(1)

        # Initialize http session object.
        self.session = None

        # Set proxy server.
        if self.proxy_addr != '':
            parse_obj = util.parse_url(self.proxy_addr)
            if self.proxy_user != '':
                self.proxy = {parse_obj.scheme: parse_obj.scheme + '://' +
                                                self.proxy_user + ':' +
                                                self.proxy_pass + '@' +
                                                parse_obj.netloc}
            else:
                self.proxy = {parse_obj.scheme: self.proxy_addr}
        else:
            self.proxy = None

        # Set HTTP request header.
        self.http_req_header = {'User-Agent': self.ua,
                                'Connection': 'keep-alive',
                                'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
                                'Accept-Encoding': 'gzip, deflate',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                'Upgrade-Insecure-Requests': '1',
                                'Content-Type': 'application/x-www-form-urlencoded'}

    # Print metasploit's symbol.
    def print_message(self, type, message):
        if os.name == 'nt':
            if type == NOTE:
                print('[+] ' + message)
            elif type == FAIL:
                print('[-] ' + message)
            elif type == WARNING:
                print('[!] ' + message)
            elif type == NONE:
                print(message)
            else:
                print('[*] ' + message)
        else:
            if type == NOTE:
                print(PRINT_NOTE + ' ' + message)
            elif type == FAIL:
                print(PRINT_FAIL + ' ' + message)
            elif type == WARNING:
                print(PRINT_WARN + ' ' + message)
            elif type == NONE:
                print(NOTE_GREEN + message + ENDC)
            else:
                print(PRINT_OK + ' ' + message)

        return

    # Print exception messages.
    def print_exception(self, e, message):
        self.print_message(WARNING, 'type:{}'.format(type(e)))
        self.print_message(WARNING, 'args:{}'.format(e.args))
        self.print_message(WARNING, '{}'.format(e))
        self.print_message(WARNING, message)
        return

    # Get current date.
    def get_current_date(self, indicate_format=None):
        if indicate_format is not None:
            date_format = indicate_format
        else:
            date_format = self.report_date_format
        return datetime.now().strftime(date_format)

    # Transform date from string to object.
    def transform_date_object(self, target_date, format=None):
        if format is None:
            return datetime.strptime(target_date, self.report_date_format)
        else:
            return datetime.strptime(target_date, format)

    # Transform date from object to string.
    def transform_date_string(self, target_date):
        return target_date.strftime(self.report_date_format)

    # Delete control character.
    def delete_ctrl_char(self, origin_text):
        clean_text = ''
        for char in origin_text:
            ord_num = ord(char)
            # Allow LF,CR,SP and symbol, character and numeric.
            if (ord_num == 10 or ord_num == 13) or (32 <= ord_num <= 126):
                clean_text += chr(ord_num)

        return clean_text

    # Convert string to integer.
    def transform_string_integer(self, origin_text):
        result = ''
        for c in origin_text:
            result += str(ord(c))

        return int(result)

    # Get all player's data.
    def get_all_players(self):
        player_data = []
        try:
            cur = self.sql.select(self.sql.conn, self.sql.state_select, (1,))
            results = cur.fetchall()
            for result in results:
                player_data.append({'id': result[0],
                                    'user_id': result[4],
                                    'password': result[5],
                                    'charge': result[2],
                                    'injustice_num': result[3],
                                    'nickname': result[6],
                                    'created_at': result[7],
                                    'level': result[8],
                                    'exp': result[9],
                                    'gold': result[10],
                                    'max_hp': result[11],
                                    'max_stamina': result[12],
                                    'max_str': result[13],
                                    'need_exp': result[14],
                                    'stamina': result[15],
                                    'staminaupdated_at': result[16],
                                    'weapon_id': result[17],
                                    'armor_id': result[18]})
        except Exception as e:
            self.print_exception(e, 'Could not read the all player\'s data from Database.')
            player_data = []

        return player_data

    # Get injustice number each player.
    def get_injustice_num(self, query):
        injustice_num = 0
        try:
            cur = self.sql.select(self.sql.conn, query, (1,))
            results = cur.fetchall()
            for result in results:
                injustice_num = result[0]
        except Exception as e:
            self.print_exception(e, 'Could not read the injustice number from Database.')

        return injustice_num

    # Get player id each player.
    def get_player_id(self, user_name):
        player_id = None
        try:
            cur = self.sql.select(self.sql.conn, self.sql.state_select_id, (user_name,))
            results = cur.fetchall()
            for result in results:
                player_id = result[0]
        except Exception as e:
            self.print_exception(e, 'Could not read the injustice number from Database.')

        return player_id

    # Get the amount of charge.
    def get_player_charge(self):
        amount_charge = 0
        try:
            cur = self.sql.select(self.sql.conn, self.sql.state_select_charge, ())
            results = cur.fetchall()
            for result in results:
                amount_charge += result[0]
        except Exception as e:
            self.print_exception(e, 'Could not read the amount of charge from Database.')

        return amount_charge

    # Get the charge amount in this epoch.
    def get_player_charge_in_this_epoch(self, epoch, player_list):
        total_charge_amount_in_this_epoch = 0
        for player in player_list:
            total_charge_amount_in_this_epoch += player.charge_amount_in_this_epoch

        self.print_message(NOTE, 'Total charge amount: {}, epoch{}'.format(total_charge_amount_in_this_epoch, epoch))
        return total_charge_amount_in_this_epoch

    # Update charge amount each player.
    def update_charge_amount(self, charge, user_name):
        try:
            self.sql.update(self.sql.conn, self.sql.state_update_charge, (charge, user_name))
        except Exception as e:
            self.print_exception(e, 'Could not update the charge amount.')

        return

    # Update status each player.
    def update_user_status(self, user_name):
        try:
            self.sql.update(self.sql.conn, self.sql.state_update_inactive, (user_name,))
        except Exception as e:
            self.print_exception(e, 'Could not update the user\'s status.')

        return

    # Update injustice number each player.
    def update_injustice_num(self, injustice_num, user_name):
        try:
            self.sql.update(self.sql.conn, self.sql.state_update_injustice_num, (injustice_num, user_name))
        except Exception as e:
            self.print_exception(e, 'Could not update the injustice number.')

        return

    # Update all data of player.
    def update_all(self, player_data):
        try:
            update_items = (player_data.created_at,
                            player_data.level,
                            player_data.exp,
                            player_data.gold,
                            player_data.max_hp,
                            player_data.max_stamina,
                            player_data.max_str,
                            player_data.need_exp,
                            player_data.stamina,
                            player_data.staminaupdated_at,
                            player_data.weapon_id,
                            player_data.armor_id,
                            player_data.user_name)
            self.sql.update(self.sql.conn, self.sql.state_update_all, update_items)
        except Exception as e:
            self.print_exception(e, 'Could not update all data of player.')

    # Insert new player.
    def insert_new_user(self, user_id, password, nick_name):
        try:
            self.sql.insert(self.sql.conn, self.sql.state_insert, (1, user_id, password, nick_name))
        except Exception as e:
            self.print_exception(e, 'Could not insert new user.')

        return

    # Judge Falsification.
    def judge_falsification(self, user_status):
        try:
            # Check integrity.
            falsify_flag = False
            if user_status.max_stamina < user_status.stamina:
                self.print_message(WARNING, 'Your max stamina is smaller than current stamina.')
                falsify_flag = True
            if falsify_flag:
                self.print_message(WARNING, 'Your max_stamina is falsified!!')
                return False

            # Check gold.
            if user_status.level <= 20 and user_status.gold > 1500:
                falsify_flag = True
            elif 20 < user_status.level <= 40 and user_status.gold > 2000:
                falsify_flag = True
            elif 40 < user_status.level <= 60 and user_status.gold > 2500:
                 falsify_flag = True
            elif 60 < user_status.level <= 80 and user_status.gold > 3000:
                falsify_flag = True
            if falsify_flag:
                self.print_message(WARNING, 'Your gold is falsified!!')
                return False

            # Check max stamina.
            if user_status.level <= 20 and user_status.max_stamina > 50:
                falsify_flag = True
            elif 20 < user_status.level <= 40 and user_status.max_stamina > 100:
                falsify_flag = True
            elif 40 < user_status.level <= 60 and user_status.max_stamina > 150:
                falsify_flag = True
            elif 60 < user_status.level <= 80 and user_status.max_stamina > 200:
                falsify_flag = True
            if falsify_flag:
                self.print_message(WARNING, 'Your max stamina is falsified!!')
                return False

            # Check max hp.
            if user_status.level <= 20 and user_status.max_hp > 100:
                falsify_flag = True
            elif 20 < user_status.level <= 40 and user_status.max_hp > 150:
                falsify_flag = True
            elif 40 < user_status.level <= 60 and user_status.max_hp > 200:
                falsify_flag = True
            elif 60 < user_status.level <= 80 and user_status.max_hp > 250:
                falsify_flag = True
            if falsify_flag:
                self.print_message(WARNING, 'Your max hp is falsified!!')
                return False

            # Check max strength.
            if user_status.level <= 20 and user_status.max_str > 50:
                falsify_flag = True
            elif 20 < user_status.level <= 40 and user_status.max_str > 100:
                falsify_flag = True
            elif 40 < user_status.level <= 60 and user_status.max_str > 150:
                falsify_flag = True
            elif 60 < user_status.level <= 80 and user_status.max_str > 200:
                falsify_flag = True
            if falsify_flag:
                self.print_message(WARNING, 'Your max strength is falsified!!')
                return False

            # Check experience.
            if user_status.level <= 20 and user_status.exp > 200:
                falsify_flag = True
            elif 20 < user_status.level <= 40 and user_status.exp > 300:
                falsify_flag = True
            elif 40 < user_status.level <= 60 and user_status.exp > 800:
                falsify_flag = True
            elif 60 < user_status.level <= 80 and user_status.exp > 2500:
                falsify_flag = True
            if falsify_flag:
                self.print_message(WARNING, 'Your experience is falsified!!')
                return False
            return True
        except Exception as e:
            self.print_exception(e, 'Could not judge Falsification.')
            time.sleep(self.loop_wait_time)
            return None

    # Judge waiting time.
    def judge_waiting_time(self, player_list):
        # Compute mean.
        tmp_level = []
        for player in player_list:
            if player.level is None:
                player.level = 0
            tmp_level.append(player.level)
        if len(tmp_level) != 0:
            mean_level = mean(tmp_level)
        else:
            mean_level = 1

        # Waiting time.
        waiting_time = 0.0
        if mean_level <= 20.0:
            waiting_time = 5
        elif 20.0 < mean_level <= 40.0:
            waiting_time = 4
        elif 40.0 < mean_level <= 60.0:
            waiting_time = 3
        elif 60.0 < mean_level <= 80.0:
            waiting_time = 2
        else:
            waiting_time = 1

        return waiting_time

    # Select gatya's gold.
    def select_gatya_gold(self, level):
        # Compute gatya's price.
        if level <= 10:
            self.print_message(WARNING, 'Selected {}G.'.format(self.min_gatya_gold))
            return self.min_gatya_gold
        else:
            self.print_message(WARNING, 'Selected {}G.'.format(level * self.std_gatya_gold))
            return level * self.std_gatya_gold

    # Execute Gatya.
    def gatya_event(self):
        # Execute Gatya in Gatya rate.
        if (random.randint(1, 10)) % self.gatya_rate == 0:
            return True
        else:
            return False

    # Initialize super rare queue.
    def init_sr_queue(self):
        self.sr_queue = deque([False, False, False])

    # Get course's ID.
    def select_battle_course_id(self, user_status, course_list):
        selected_course_id = -1
        try:
            if user_status.stamina >= course_list[4]['stamina']*self.battle_stamina_rate:
                selected_course_id = course_list[4]['id']
            elif user_status.stamina >= course_list[3]['stamina']*self.battle_stamina_rate:
                selected_course_id = course_list[3]['id']
            elif user_status.stamina >= course_list[2]['stamina']*self.battle_stamina_rate:
                selected_course_id = course_list[2]['id']
            elif user_status.stamina >= course_list[1]['stamina']*self.battle_stamina_rate:
                selected_course_id = course_list[1]['id']
            elif user_status.stamina >= course_list[0]['stamina']:
                selected_course_id = course_list[0]['id']
            return selected_course_id
        except Exception as e:
            self.print_exception(e, 'Could not select course.')
            time.sleep(self.loop_wait_time)
            return False

    # Get player's wait time.
    def get_player_wait_time(self, level):
        return float((self.max_player_level - level)/10)

    # Decode parameter (name and value).
    def decode_parameter(self, params):
        parameter = {}
        for item in params.items():
            parameter[urllib.parse.unquote(item[0])] = urllib.parse.unquote(item[1])

        return parameter

    # Create http session.
    def create_http_session(self):
        # Session object for sending request.
        session = requests.session()
        if self.proxy is not None:
            session.proxies = self.proxy

        return session

    # Get ranking information.
    def get_ranking(self, session, sort='level'):
        self.http_req_header['Content-Type'] = self.api_ranking_ctype

        url = ''
        if sort == 'level':
            url = self.api_ranking_url + '?sort=1'
        elif sort == 'stamina':
            url = self.api_ranking_url + '?sort=2'
        elif sort == 'gold':
            url = self.api_ranking_url + '?sort=3'
        elif sort == 'exp':
            url = self.api_ranking_url + '?sort=4'
        elif sort == 'weapon':
            url = self.api_ranking_url + '?sort=5'
        else:
            url = self.api_ranking_url 

        status, response = self.send_request(session,
                                             self.api_ranking_method,
                                             url,
                                             self.http_req_header,
                                             None)

        if status is False:
            self.print_message(FAIL, 'Could not connect "ranking" API.')
            time.sleep(self.loop_wait_time)
            return None, None, None
        else:
            self.print_message(OK, 'Complete getting ranking information.')
            return response, None, None

    # New user registration.
    def user_registration(self, session):
        user_id = hashlib.sha256(b'userid' + self.get_current_date().encode() + bytes(random.randint(1, 1000000))).hexdigest()
        password = hashlib.sha256(b'pass' + self.get_current_date().encode()).hexdigest()

        # Choice nick name from list.
        with codecs.open(os.path.join(self.full_path, 'nickname.txt'), mode='r', encoding='utf-8') as fin:
            nickname_list = fin.read().split('\n')
        nick_name = random.choice(nickname_list) + '_' + hashlib.md5().hexdigest()[:10]
        self.api_new_user_params['user_name'] = user_id
        self.api_new_user_params['password'] = password
        self.api_new_user_params['nick_name'] = nick_name
        self.http_req_header['Content-Type'] = self.api_new_user_ctype
        status, response = self.send_request(session,
                                             self.api_new_user_method,
                                             self.api_new_user_url,
                                             self.http_req_header,
                                             self.api_new_user_params)

        if status is False:
            self.print_message(FAIL, 'Could not connect "new_user" API.')
            time.sleep(self.loop_wait_time)
            return None, None, None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None, None, None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None, None, None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None, None, None
        else:
            #self.print_message(OK, 'Complete registration.')
            return user_id, password, nick_name

    # User Login.
    def user_login(self, session, user_id, password):
        self.api_login_params['user_name'] = user_id
        self.api_login_params['password'] = password
        self.http_req_header['Content-Type'] = self.api_login_ctype
        status, response = self.send_request(session,
                                             self.api_login_method,
                                             self.api_login_url,
                                             self.http_req_header,
                                             self.api_login_params)
        
        if status is False:
            self.print_message(FAIL, 'Could not connect "login" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None
        elif 'session_id' not in response.keys():
            self.print_message(WARNING, '{}'.format('"session_id" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response['session_id']

    # Get Course List
    def get_course(self, session):
        self.http_req_header['Content-Type'] = self.api_courseget_ctype
        status, response = self.send_request(session,
                                             self.api_courseget_method,
                                             self.api_courseget_url,
                                             self.http_req_header,
                                             self.api_courseget_params)
        
        if status is False:
            self.print_message(FAIL, 'Could not connect "Course" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None
        elif 'course' not in response.keys():
            self.print_message(WARNING, '{}'.format('"course" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response['course']

    # Set Course
    def set_course(self, session, course_id):
        self.api_courseset_params['id'] = course_id
        self.http_req_header['Content-Type'] = self.api_courseset_ctype
        status, response = self.send_request(session,
                                             self.api_courseset_method,
                                             self.api_courseset_url,
                                             self.http_req_header,
                                             self.api_courseset_params)
        
        if status is False:
            self.print_message(FAIL, 'Could not connect "Course" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None
        elif 'cost' not in response.keys():
            self.print_message(WARNING, '{}'.format('"cost" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'course' not in response.keys():
            self.print_message(WARNING, '{}'.format('"course" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'enemy' not in response.keys():
            self.print_message(WARNING, '{}'.format('"enemy" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'msg' not in response.keys():
            self.print_message(WARNING, '{}'.format('"msg" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'phase' not in response.keys():
            self.print_message(WARNING, '{}'.format('"phase" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'player' not in response.keys():
            self.print_message(WARNING, '{}'.format('"player" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'turn' not in response.keys():
            self.print_message(WARNING, '{}'.format('"turn" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'tot_damage' not in response.keys():
            self.print_message(WARNING, '{}'.format('"tot_damage" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'stamina_recovery' not in response.keys():
            self.print_message(WARNING, '{}'.format('"stamina_recovery" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response


    # Access to BattleAPI normally
    def battle(self, session, battle_info):
        self.http_req_header['Content-Type'] = self.api_battle_ctype
        status, response = self.send_request(session,
                                             self.api_battle_method,
                                             self.api_battle_url,
                                             self.http_req_header,
                                             battle_info)
        
        if status is False:
            self.print_message(FAIL, 'Could not connect "Battle" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None
        elif 'cost' not in response.keys():
            self.print_message(WARNING, '{}'.format('"cost" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'course' not in response.keys():
            self.print_message(WARNING, '{}'.format('"course" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'enemy' not in response.keys():
            self.print_message(WARNING, '{}'.format('"enemy" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'msg' not in response.keys():
            self.print_message(WARNING, '{}'.format('"msg" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'phase' not in response.keys():
            self.print_message(WARNING, '{}'.format('"phase" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'player' not in response.keys():
            self.print_message(WARNING, '{}'.format('"player" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'turn' not in response.keys():
            self.print_message(WARNING, '{}'.format('"turn" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'tot_damage' not in response.keys():
            self.print_message(WARNING, '{}'.format('"tot_damage" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response


    # Cheat for BattleAPI
    def cheat_battle(self, session, battle_info):
        battle_info['player']['hp'] = 99
        battle_info['player']['str'] = 99
        battle_info['enemy']['exp'] = 1000
        self.http_req_header['Content-Type'] = self.api_battle_ctype
        status, response = self.send_request(session,
                                             self.api_battle_method,
                                             self.api_battle_url,
                                             self.http_req_header,
                                             battle_info)
        
        if status is False:
            self.print_message(FAIL, 'Could not connect "Battle" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None
        elif 'cost' not in response.keys():
            self.print_message(WARNING, '{}'.format('"cost" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'course' not in response.keys():
            self.print_message(WARNING, '{}'.format('"course" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'enemy' not in response.keys():
            self.print_message(WARNING, '{}'.format('"enemy" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'msg' not in response.keys():
            self.print_message(WARNING, '{}'.format('"msg" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'phase' not in response.keys():
            self.print_message(WARNING, '{}'.format('"phase" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'player' not in response.keys():
            self.print_message(WARNING, '{}'.format('"player" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'turn' not in response.keys():
            self.print_message(WARNING, '{}'.format('"turn" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'tot_damage' not in response.keys():
            self.print_message(WARNING, '{}'.format('"tot_damage" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response


    # User Login SQLi
    def user_login_sqli(self, session, password):
        prefix = hashlib.sha256(b'userid' + self.get_current_date().encode() + bytes(random.randint(1, 1000000))).hexdigest()
        self.api_login_params['user_name'] = prefix + "user_id"
        self.api_login_params['password'] = prefix + password
        self.http_req_header['Content-Type'] = self.api_login_ctype
        status, response = self.send_request(session,
                                             self.api_login_method,
                                             self.api_login_url,
                                             self.http_req_header,
                                             self.api_login_params)
        
        if status is False:
            self.print_message(FAIL, 'Could not connect "login" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None
        elif 'session_id' not in response.keys():
            self.print_message(WARNING, '{}'.format('"session_id" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response


    # Create User SQLi
    def user_registration_sqli(self, session, user_id):
        prefix = hashlib.sha256(b'userid' + self.get_current_date().encode() + bytes(random.randint(1, 1000000))).hexdigest()
        self.api_new_user_params['user_name'] = prefix + user_id
        self.api_new_user_params['password'] = prefix + 'password'
        self.api_new_user_params['nick_name'] = prefix + 'nick_name'
        self.http_req_header['Content-Type'] = self.api_new_user_ctype
        status, response = self.send_request(session,
                                             self.api_new_user_method,
                                             self.api_new_user_url,
                                             self.http_req_header,
                                             self.api_new_user_params)
        
        if status is False:
            self.print_message(FAIL, 'Could not connect "create" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response


    # Get Player Info.
    def get_player_info(self, session):
        self.http_req_header['Content-Type'] = self.api_pinfo_ctype
        status, response = self.send_request(session,
                                             self.api_pinfo_method,
                                             self.api_pinfo_url,
                                             self.http_req_header,
                                             self.api_pinfo_params)
        # debug
        #self.print_message(self.warning, 'response: {}'.format(response))

        if status is False:
            self.print_message(FAIL, 'Could not connect "player" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None
        elif 'id' not in response.keys():
            self.print_message(WARNING, '{}'.format('"id" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response

    # Upload Image.
    def upload_player_image(self, session, file_name, file_data):
        self.api_imgupload_params['file_name'] = file_name
        self.api_imgupload_params['file_data'] = file_data
        self.http_req_header['Content-Type'] = self.api_imgupload_ctype
        status, response = self.send_request(session,
                                             self.api_imgupload_method,
                                             self.api_imgupload_url,
                                             self.http_req_header,
                                             self.api_imgupload_params)
        # debug
        #self.print_message(self.warning, 'response: {}'.format(response))

        if status is False:
            self.print_message(FAIL, 'Could not connect "upload" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response

    # Charge Gold
    def charge_gold(self, session, charge_amount):
        self.api_charge_params['price'] = charge_amount
        self.http_req_header['Content-Type'] = self.api_charge_ctype
        status, response = self.send_request(session,
                                             self.api_charge_method,
                                             self.api_charge_url,
                                             self.http_req_header,
                                             self.api_charge_params)
        # debug
        #self.print_message(self.warning, 'response: {}'.format(response))

        if status is False:
            self.print_message(FAIL, 'Could not connect "charge" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response
    
    # Recovery Stamina
    def recovery_stamina(self, session, recovery_cost):
        self.api_recovery_params['price'] = recovery_cost
        self.http_req_header['Content-Type'] = self.api_recovery_ctype
        status, response = self.send_request(session,
                                             self.api_recovery_method,
                                             self.api_recovery_url,
                                             self.http_req_header,
                                             self.api_recovery_params)
        # debug
        #self.print_message(self.warning, 'response: {}'.format(response))

        if status is False:
            self.print_message(FAIL, 'Could not connect "recovery" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response
    
    # Do the Gacha
    def get_gacha(self, session, charge_amount):
        self.api_gacha_params['gold'] = charge_amount
        self.http_req_header['Content-Type'] = self.api_gacha_ctype
        status, response = self.send_request(session,
                                             self.api_gacha_method,
                                             self.api_gacha_url,
                                             self.http_req_header,
                                             self.api_gacha_params)
        # debug
        #self.print_message(self.warning, 'response: {}'.format(response))

        if status is False:
            self.print_message(FAIL, 'Could not connect "gacha" API.')
            time.sleep(self.loop_wait_time)
            return None
        elif type(response) != dict:
            self.print_message(WARNING, '{}'.format('"response" is not dict.'))
            time.sleep(self.loop_wait_time)
            return None
        elif 'result' not in response.keys():
            self.print_message(WARNING, '{}'.format('"result" is not included in "response".'))
            time.sleep(self.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.print_message(WARNING, '{}'.format(response['msg']))
            time.sleep(self.loop_wait_time)
            return None
        else:
            return response

    # Judge hacked target web site.
    def judge_hacked(self, response, regex_hacked):
        status = True
        if re.search(regex_hacked, response) is not None:
            self.print_message(WARNING, 'This site is hacked : including "{}"'.format(regex_hacked))
            status = False
        return status


    # Get file on the repository server.
    def get_repo_file(self, file_type='readme'):
        if file_type == 'readme':
            status, response = self.send_request(self.create_http_session(), 'get', self.repo_url_readme, self.http_req_header, {})
            return status, response, None
        else:
            res_hash = None
            status, response = self.send_request(self.create_http_session(), 'get', self.repo_url_csv, self.http_req_header, {})
            if status:
                res_hash = hashlib.sha256(response.encode()).hexdigest()
            return status, None, res_hash

    # Get Web site information (url, score).
    def get_web_info(self, site_type):
        target_url = ''
        score = 0
        keywords = []
        if site_type == 'corp':
            target_url = self.web_corporate_url
            score = self.web_corporate_score
            keywords = self.web_corporate_keywords
        elif site_type == 'fan':
            target_url = self.web_fansite_url
            score = self.web_fansite_score
            keywords = self.web_fansite_keywords
        elif site_type == 'saiyo':
            target_url = self.web_saiyo_url
            score = self.web_saiyo_score
            keywords = self.web_saiyo_keywords
        elif site_type == 'bbs':
            target_url = self.web_bbs_url
            score = self.web_bbs_score
            keywords = self.web_bbs_keywords
        elif site_type == 'inquiry':
            target_url = self.web_inquiry_url
            score = self.web_inquiry_score
            keywords = self.web_inquiry_keywords
        else:
            self.print_message(WARNING, '{} is not found.'.format(site_type))
            self.print_message(WARNING, 'Selected "corp" instead of {}.'.format(site_type))
            target_url = self.web_corporate_url
            score = self.web_corporate_score
            keywords = self.web_corporate_keywords

        return target_url, score, keywords

    # Send http request.
    def send_request(self, session, method, target_url, header, body_param):
        res = None

        # Decode parameter (name and value).
        if header['Content-Type'].lower() != 'application/json':
            body_param = self.decode_parameter(body_param)

        # Send request and receive response.
        try:
            res = None
            if method.lower() == 'get':
                res = session.get(target_url,
                                  data=body_param,
                                  headers=header,
                                  timeout=self.con_timeout,
                                  allow_redirects=True)
            elif method.lower() == 'post':
                if header['Content-Type'].lower() != 'application/json':
                    res = session.post(target_url,
                                       data=body_param,
                                       headers=header,
                                       timeout=self.con_timeout,
                                       allow_redirects=True)
                else:
                    res = session.post(target_url,
                                       json.dumps(body_param),
                                       headers=header,
                                       timeout=self.con_timeout,
                                       allow_redirects=True)
            else:
                self.print_message(WARNING, 'Invalid method : {}.'.format(method))
                return False, {}

            # Check response code.
            if res.status_code >= 400:
                self.print_message(FAIL, 'Occur error: status={}'.format(res.status_code))
                return False, res.text

            # Convert from string to dictionary.
            if 'application/json' in res.headers['Content-Type'].lower():
                return True, json.loads(res.text)
            else:
                return True, res.text

        except Exception as e:
            self.print_exception(e, 'Accessing is failure : {}'.format(target_url))
            return False, {}


    # Send simple http get request for user list.
    def get_request4userlist(self, target_url, session=None):
        res = None

        if session is None:
            session = self.create_http_session()

        # Send request and receive response.
        try:
            res = session.get(target_url,
                                timeout=self.con_timeout,
                                allow_redirects=True)

            # Check response code.
            if res.status_code == 401 or res.status_code == 403 or res.status_code ==404 or res.status_code != 410:
                return True, res
            else:
                self.print_message(FAIL, 'Occur error: status={}'.format(res.status_code))
                return False, res


        except Exception as e:
            self.print_exception(e, 'Accessing is failure : {}'.format(target_url))
            return False, {}


    # Send simple http get request.
    def get_request(self, target_url, session=None):
        res = None

        if session is None:
            session = self.create_http_session()

        # Send request and receive response.
        try:
            res = session.get(target_url,
                                timeout=self.con_timeout,
                                allow_redirects=True)

            # Check response code.
            if res.status_code >= 400:
                self.print_message(FAIL, 'Occur error: status={}'.format(res.status_code))
                return False, res

            return True, res

        except Exception as e:
            self.print_exception(e, 'Accessing is failure : {}'.format(target_url))
            return False, {}

    # Send simple http post request.
    def post_request(self, target_url, body_param, session=None):
        res = None
        header={'Content-Type': 'application/x-www-form-urlencoded'}

        if session is None:
            session = self.create_http_session()

        # Send request and receive response.
        try:
            res = session.post(target_url,
                                data=body_param,
                                headers=header,
                                timeout=self.con_timeout,
                                allow_redirects=True)

            # Check response code.
            if res.status_code >= 400:
                self.print_message(FAIL, 'Occur error: status={}'.format(res.status_code))
                return False, res

            return True, res

        except Exception as e:
            self.print_exception(e, 'Accessing is failure : {}'.format(target_url))
            return False, {}
    
    # Send ssh request.  
    def ssh_request(self, target="127.0.0.1", cmd="whoami", user="user", pwd="password", key=None):
        if key == None:
            # is password authentication
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(target, username=user, password=pwd)
                stdin, stdout, stderr = ssh.exec_command(cmd)
                result = stdout.read()
                ssh.close()
                return result
            except Exception as e:
                #self.print_exception(e, 'Accessing is failure : {}'.format(target))
                return None
        else:
            # is public key authentication
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(target, username=user, key_filename=key)
                stdin, stdout, stderr = ssh.exec_command(cmd)
                result = stdout.read()
                ssh.close()
                return result
            except Exception as e:
                #self.print_exception(e, 'Accessing is failure : {}'.format(target))
                return None

    # Save game status to DB (sqlite3).
    def insert_attack_judge_result_to_db(self, technical_point):
        try:
            insert_data = (technical_point, self.get_current_date())
            self.sql.insert(self.sql.conn, self.sql.state_insert_judge_attack_result, insert_data)
        except Exception as e:
            self.print_exception(e, 'Could not insert attack judge result.')

    # Select latest one record from judge attack table.
    def get_technical_point(self):
        cur = self.sql.select(self.sql.conn, self.sql.state_select_judge_attack_result, ())
        return cur.fetchone()
