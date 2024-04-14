#!/usr/bin/env python
# coding: UTF-8
import subprocess
import requests

class AtkStopProcess(object):
    def __init__(self, host="127.0.0.1", port="8000", debug=False):
        self.host=host
        self.port=port
        self.debug = debug
        self.description = "The module can stop some generated processes."
        self.url = "http://" + host + ":" + port

    def __str__(self):
        return 'AtkStopProcess object (description: %s)' % (self.description)

    __repr__ = __str__


    def stop(self):
        try:
            sub1 = subprocess.Popen(['killall', 'perl'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            sub2 = subprocess.Popen(['killall', 'nc'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            session = requests.Session()  
            session.get(self.url + "/stopserver")
            return True
        except requests.exceptions.RequestException as e:
            #print(e)
            return True
        