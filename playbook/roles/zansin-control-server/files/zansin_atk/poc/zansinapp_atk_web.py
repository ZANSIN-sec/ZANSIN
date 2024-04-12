#!/usr/bin/env python
# coding: UTF-8
import sys
import os
import subprocess
import requests


class AtkWebServer(object):
    def __init__(self, host="127.0.0.1", port="8000", debug=False):
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.host = host
        self.port = port
        self.debug = debug
        self.description = "The module can be do the web server."
        self.url = "http://" + host + ":" + port

    def __str__(self):
        return 'AtkWebServer object (server: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__

    def startserver(self):
        sub = subprocess.Popen([sys.executable, os.path.join(self.full_path, 'zansinapp_atk_aiohttp.py'), self.host, self.port])
        return True
    
    def stopserver(self):
        try:
            session = requests.Session()  
            session.get(self.url + "/stopserver")
            return True
        except requests.exceptions.RequestException as e:
            #print(e)
            return True
