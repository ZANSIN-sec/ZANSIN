#!/usr/bin/env python
# coding: UTF-8
import sys
import subprocess
import requests


class AtkDnsServer(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.description = "The module can be do the dns c2 server."

    def __str__(self):
        return 'AtkDnsServer object (server: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__

    def startserver(self):
        # The server automaticaly stop after 120 seconds.
        sub = subprocess.Popen(['tools/c2s/start_c2s.sh'])
        return True
    


