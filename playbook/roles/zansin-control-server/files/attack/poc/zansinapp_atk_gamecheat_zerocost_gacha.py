#!/usr/bin/env python
# coding: UTF-8
import os
import sys
import subprocess

class AtkGameCheatZeroCostGacha(object):
    def __init__(self, utility, host="127.0.0.1", debug=False):
        self.utility = utility
        self.host = host
        self.ua = utility.ua
        self.debug = True
        self.description = "The module can be zero-cost gacha cheat if a bug of GachaAPI is not fix yet."

    def __str__(self):
        return 'AtkGameCheatZeroCostGacha object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__


    def sendattack(self, interval=0.1, num=10000):
        if self.debug:
            sub = subprocess.Popen([sys.executable, os.path.join(self.utility.full_path, 'poc/zansinapp_atk_cheat_gacha.py'), self.host, str(interval), str(num), self.ua])
        else:
            sub = subprocess.Popen([sys.executable, os.path.join(self.utility.full_path, 'poc/zansinapp_atk_cheat_gacha.py'), self.host, str(interval), str(num), self.ua], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True


