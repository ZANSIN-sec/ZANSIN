#!/usr/bin/env python
# coding: UTF-8
import nmap


class AtkNmap(object):
    def __init__(self, host="127.0.0.1", debug=False):
        self.host = host
        self.debug = debug
        self.description = "The module can be do the Nikto."

    def __str__(self):
        return 'AtkNmap object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__

    def sendattack(self, port="1-1023,2375,3000,3306,5555,6379,8000-9000,10000"):
        n = nmap.PortScanner()
        n.scan(self.host, port, '-sS -Pn')
        return n[self.host]['tcp'].keys()
