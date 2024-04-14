#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import re
import base64


class CheckDebug(object):
    def __init__(self, utility, host="127.0.0.1", path="/", debug=False):
        self.utility = utility
        self.utility.target = host
        self.point = 0.0
        self.name = 'CheckDebug'
        self.host = host
        self.path = path
        self.debug = debug
        self.description = "The module can check if the web application is currently working and also check the behavior restriction to access for debug page."
        self.url1 = self.utility.debug1_url # ex: http://127.0.0.1/
        self.url2 = self.utility.debug2_url # ex: http://127.0.0.1/


    def __str__(self):
        return '%s object (target: %s, %s description: %s)' % (self.name, self.url1, self.url2, self.description)

    __repr__ = __str__

    def test(self):

        return_values = {
            "host": self.host,
            "url": "%s, %s" % (self.url1, self.url2),
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
        # Check Debug API
        #=======================================================================
        status, res = self.utility.get_request(self.url1, session1)
        if status:
            # check response
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: Debug API 1 is currently open(target: %s)' % (self.name, self.url1))
            return_values["description"] = "Debug API 1 is currently open."
            return_values["result"] = False
        else:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: Debug API 1 is currently closed(target: %s)' % (self.name, self.url1))
            return_values["description"] = "Debug API 1 is currently closed."
            return_values["result"] = True
            self.point += float(self.utility.point_debug1)

        status, res = self.utility.get_request(self.url2, session1)
        if status:
            # check response
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: Debug API 2 is currently open(target: %s)' % (self.name, self.url2))
            if self.point > 0:
                return_values["description"] = return_values["description"] + " but Debug API 2 is currently open."
            else:
                return_values["description"] = "Debug APIs are currently open."
            #son_data["result"] = False
        else:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: Debug API 2 is currently closed(target: %s)' % (self.name, self.url2))
            if self.point > 0:
                return_values["description"] = "Debug APIs are currently closed."
            return_values["result"] = True
            self.point += float(self.utility.point_debug2)

        return_values["point"] = self.point
        return return_values
