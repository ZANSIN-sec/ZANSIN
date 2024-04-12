#!/usr/bin/env python
# coding: UTF-8
import sys
import subprocess


class AtkNikto(object):
    def __init__(self, utility, host="127.0.0.1", niktopath="/usr/bin/nikto", debug=False):
        self.host = host
        self.debug = debug
        self.utility = utility
        self.utility.target = host
        self.description = "The module can be do the Nikto."
        self.nikto = niktopath

    def __str__(self):
        return 'AtkNikto object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__


    def sendattack(self):
        ua = self.utility.ua

        sub = subprocess.Popen([self.nikto, '-h', self.host, '-useragent', ua, "-ask", "no", "-ipv4", "-timeout", str(2)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True


