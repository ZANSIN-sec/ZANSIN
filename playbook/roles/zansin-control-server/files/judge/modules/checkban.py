#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
#from util import Utility


class CheckBan(object):
    def __init__(self, utility, host="127.0.0.1", path="/", debug=False):
        self.utility = utility
        self.utility.target = host
        self.name = 'CheckBan'
        self.point = float(self.utility.point_userlist)
        self.host = host
        self.path = path
        self.debug = debug
        self.description = "The module can check if the web application is currently working and also check the behavior restriction to access for user_list page."
        self.url = self.utility.ban_url # ex: http://127.0.0.1

    def __str__(self):
        return 'CheckBan object (target: %s, description: %s)' % (self.url, self.description)

    __repr__ = __str__

    def test(self):
        pattern = self.utility.ban_keyword
        rpattern = re.compile(re.escape(pattern))

        return_values = {
            "host": self.host,
            "url": self.url,
            "status_code": 0,
            "length": 0,
            "description": "",
            "pass_check": 0,
            "result": False,
            "point" : 0.0
        }


        #=======================================================================
        # User1 registration and login
        #=======================================================================

        # User1 registration
        session1 = self.utility.create_http_session()
        user_id1, password1, nick_name1 = self.utility.user_registration(session1)

        #utility.print_message(utility.none, 'user_id: %s, pass: %s, name: %s' % (user_id1, password1, nick_name1))

        if user_id1 == None or password1 == None or nick_name1 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: user1 registration failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "user1 registration failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user1 registration OK(target: %s)' % (self.name, self.url))
            return_values["user_id"] = user_id1
            return_values["password"] = password1
            return_values["nick_name"] = nick_name1
        
        # User1 Login
        session_id1 = self.utility.user_login(session1, user_id1, password1)
        if session_id1 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: user1 login failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "user1 registration OK but login failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user1 login OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "user1 registration and login OK."
            return_values["session_id"] = session_id1
        


        #=======================================================================
        # Check user_list page
        #=======================================================================
        status, response = self.utility.get_request4userlist(self.url)
        return_values["status_code"] = response.status_code
        return_values["length"] = response.headers.get('content-length')

        if response.status_code == 200:
            content = response.text
            if rpattern.search(content):
                # BanPage detected
                if self.debug:
                    self.utility.print_message(self.utility.fail, '%s: user_list page was detected(target: %s)' % (self.name, self.url))
                return_values["description"] = "/user_list was detected."
                return_values["result"] = False
                return return_values
            else:
                # BanPage not detected
                if self.debug:
                    self.utility.print_message(self.utility.note, '%s: user_list page was not detected(target: %s)' % (self.name, self.url))
                return_values["description"] = "/user_list was not detected."
                return_values["result"] = True
                return_values["point"] = self.point
                return return_values
        else:
            # request failed
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user_list page was Auth required or NotFound(target: %s, status: %s)' % (self.name, self.url, response.status_code))
            return_values["description"] = "user_list page was Auth required or NotFound."
            return_values["result"] = True
            return_values["point"] = self.point
            return return_values