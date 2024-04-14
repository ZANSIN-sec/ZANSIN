#!/usr/bin/env python
# coding: UTF-8
import os
import sys
import subprocess
import requests

class AtkDnsServer(object):
    def __init__(self, utility, debug=False):
        self.utility = utility
        self.debug = debug
        self.description = "The module can be do the dns c2 server."

    def __str__(self):
        return 'AtkDnsServer object (server: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__


    def startserver(self, server):
        # The server automaticaly stop after 120 seconds.
        if self.debug:
            sub = subprocess.Popen([os.path.join(self.utility.full_path, 'tools/c2s/start_c2s.sh'), server])
        else:
            #sub = subprocess.Popen([os.path.join(self.utility.full_path, 'tools/c2s/start_c2s.sh'), server])
            sub = subprocess.Popen([os.path.join(self.utility.full_path, 'tools/c2s/start_c2s.sh'), server], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    


