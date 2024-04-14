#!/usr/bin/env python
# coding: UTF-8
import os
import sys
import subprocess

class AtkNikto(object):
    def __init__(self, utility, host="127.0.0.1", niktopath="/usr/bin/nikto", debug=False):
        self.utility = utility
        self.host = host
        self.debug = debug
        self.description = "The module can be do the Nikto."
        self.nikto = niktopath
        self.conf = os.path.join(utility.full_path, "nikto.conf")

    def __str__(self):
        return 'AtkNikto object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__


    def sendattack(self):
        if self.debug:
            sub = subprocess.Popen([self.nikto, '-h', self.host, '-conf', self.conf, "-ask", "no", "-timeout", str(2)])
        else:
            sub = subprocess.Popen([self.nikto, '-h', self.host, '-conf', self.conf, "-ask", "no", "-timeout", str(2)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True


