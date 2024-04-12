#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CheckSSH(object):
    def __init__(self, utility, host="127.0.0.1", debug=False):
        self.utility = utility
        self.utility.target = host
        self.name = 'CheckSSH'
        self.point = float(self.utility.point_loginssh)
        self.host = host
        self.users = self.utility.ssh_users
        self.password = self.utility.ssh_password
        self.cmd = self.utility.ssh_cmd
        self.count = self.users.__len__()
        self.debug = debug
        self.description = "The module can access to a host on the SSH."


    def __str__(self):
        return 'CheckSSH object (target: %s, description: %s)' % (self.host, self.description)

    __repr__ = __str__

    def test(self):
  
        return_values = {
            "host": self.host,
            "description": "",
            "result": False,
            "point" : 0.0
        }

        # SSH connect
        success_count = 0
        for user in self.users:
            result = self.utility.ssh_request(self.host, self.cmd, user, self.password)
            if self.debug:
                self.utility.print_message(self.utility.note, 'Try to access to the host on the SSH(target: %s, user: %s)' % (self.host, user))
            if result == None:
                if self.debug:
                    self.utility.print_message(self.utility.fail, 'CheckSSH: Accessing is failure(target: %s, user: %s)' % (self.host, user))
            else:
                
                if self.debug:
                    self.utility.print_message(self.utility.note, 'CheckSSH: Accessing is success(target: %s, user: %s)' % (self.host, user))
                success_count += 1
        
        if success_count > 0:
            return_values["description"] = "SSH access was succeed[count: %d/%d]" % (success_count, self.count)
            return_values["result"] = False
        else:
            return_values["description"] = "SSH access was failed[count: %d/%d]" % (success_count, self.count)
            return_values["result"] = True
            return_values["point"] = self.point
        return return_values