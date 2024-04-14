#!/usr/bin/env python
# coding: UTF-8
import subprocess

class AtkReverseShell(object):
    def __init__(self, utility, host="127.0.0.1", cmd="ls", debug=False):
        self.utility = utility
        self.host = host
        self.debug = debug
        self.description = "The module can be do the bash."
        self.cmd = cmd

    def __str__(self):
        return 'AtkReverseShell object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__


    def sendattack(self):
        sub = subprocess.Popen(['bash', '-c', self.cmd], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True


