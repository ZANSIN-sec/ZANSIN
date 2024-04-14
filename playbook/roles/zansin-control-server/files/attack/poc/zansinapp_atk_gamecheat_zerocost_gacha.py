#!/usr/bin/env python
# coding: UTF-8
import sys
import subprocess


class AtkGameCheatZeroCostGacha(object):
    def __init__(self, host="127.0.0.1", debug=False):
        self.host = host
        self.debug = debug
        self.description = "The module can be zero-cost gacha cheat if a bug of GachaAPI is not fix yet."

    def __str__(self):
        return 'AtkGameCheatZeroCostGacha object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__

    def sendattack(self, interval=0.1, num=10000):
        sub = subprocess.Popen([sys.executable, 'poc/zansinapp_atk_cheat_gacha.py', self.host, str(interval), str(num)])
        return True
