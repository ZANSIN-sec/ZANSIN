#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import re
import base64


class CheckNewUser(object):
    def __init__(self, utility, host="127.0.0.1", path="/", debug=False):
        self.utility = utility
        self.utility.target = host
        self.point = 0.0
        self.name = 'CheckNewUser'
        self.host = host
        self.path = path
        self.debug = debug
        self.description = "The module can check if the web application is currently working and also check the behavior restriction to access for new_user.php"
        self.url = self.utility.newuser_url # ex: http://127.0.0.1/


    def __str__(self):
        return '%s object (target: %s, description: %s)' % (self.name, self.url, self.description)

    __repr__ = __str__

    def test(self):

        return_values = {
            "host": self.host,
            "url": "%s" % (self.url),
            "status_code": 0,
            "length": 0,
            "description": "",
            "pass_check": 0,
            "result": False,
            "user_id": "",
            "password": "",
            "nick_name": "",
            "session_id": "",
            "point" : 0.0
        }

        #=======================================================================
        # User1 registration and login
        #=======================================================================

        # User1 registration
        session1 = self.utility.create_http_session()
        user_id1, password1, nick_name1 = self.utility.user_registration(session1)

        #self.utility.print_message(self.utility.none, 'user_id: %s, pass: %s, name: %s' % (user_id1, password1, nick_name1))

        if user_id1 == None or password1 == None or nick_name1 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: user1 registration failed(target: %s)' % (self.name, return_values["url"]))
            return_values["description"] = "user1 registration failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user1 registration OK(target: %s)' % (self.name, return_values["url"]))
            return_values["user_id"] = user_id1
            return_values["password"] = password1
            return_values["nick_name"] = nick_name1
        
        # User Login
        session_id = self.utility.user_login(session1, user_id1, password1)
        if session_id == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: user1 login failed(target: %s)' % (self.name, return_values["url"]))
            return_values["description"] = "user1 registration OK but login failed normally."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user1 login OK(target: %s)' % (self.name, return_values["url"]))
            return_values["description"] = "user1 registration and login OK."
            return_values["session_id"] = session_id


        #=======================================================================
        # Check new_user.php
        #=======================================================================
        status, res = self.utility.get_request(self.url, session1)
        
        if status:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: new_user.php is found currently(target: %s)' % (self.name, self.url))
            return_values["description"] = "new_user.php is found currently."
            return_values["result"] = False
        else:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: new_user.php is not found currently(target: %s)' % (self.name, self.url))
            return_values["description"] = "new_user.php is not found currently."
            return_values["result"] = True
            self.point += float(self.utility.point_newuser)

        return_values["point"] = self.point
        return return_values
