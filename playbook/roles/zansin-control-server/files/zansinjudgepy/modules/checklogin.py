#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CheckLogin(object):
    def __init__(self, utility, host="127.0.0.1", path="/", debug=False):
        self.utility = utility
        self.utility.target = host
        self.host = host
        self.path = path
        self.debug = debug
        self.description = "The module can check if the web application is currently working and also check the behavior of create user and login access."
        self.url = self.utility.api_login_url # ex: http://127.0.0.1

    def __str__(self):
        return 'CheckLogin object (target: %s, description: %s)' % (self.url, self.description)

    __repr__ = __str__

    def test(self):
  
        return_values = {
            "host": self.host,
            "url": self.url,
            "status_code": 0,
            "length": 0,
            "description": "",
            "pass_check": 0,
            "result": False,
            "user_id": "",
            "password": "",
            "nick_name": "",
            "session_id": ""
        }

        # User registration
        session = self.utility.create_http_session()
        user_id, password, nick_name = self.utility.user_registration(session)

        #utility.print_message(utility.none, 'user_id: %s, pass: %s, name: %s' % (user_id, password, nick_name))

        if user_id == None or password == None or nick_name == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, 'CheckLogin: user registration failed(target: %s)' % (self.url))
            return_values["description"] = "user registration failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, 'CheckLogin: user registration OK(target: %s)' % (self.url))
            return_values["user_id"] = user_id
            return_values["password"] = password
            return_values["nick_name"] = nick_name
        
        # User Login
        session_id = self.utility.user_login(session, user_id, password)
        if session_id == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, 'CheckLogin: user login failed(target: %s)' % (self.url))
            return_values["description"] = "user registration OK but login failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, 'CheckLogin: user login OK(target: %s)' % (self.url))
            return_values["description"] = "user registration and login OK."
            return_values["session_id"] = session_id
            return_values["result"] = True
            return return_values
        