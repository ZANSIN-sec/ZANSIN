#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import time


class CheckNewUserSQLi(object):
    def __init__(self, utility, host="127.0.0.1", path="/", debug=False):
        self.utility = utility
        self.utility.target = host
        self.point = float(self.utility.point_loginsqli)
        self.name = 'CheckCreateUserSQLi'
        self.host = host
        self.path = path
        self.debug = debug
        self.description = "The module can check if the web application is currently working and also check SQLi at the create user function."
        #self.b64data = 'eyJ1c2VyX25hbWUiOiJhJyBhbmQgc2xlZXAoMTApOyAtLSAiLCJwYXNzd29yZCI6ImEiLCJuaWNrX25hbWUiOiJhIn0=' #{"user_name":"a' and sleep(10); -- ","password":"a","nick_name":"a"}
        self.b64data = 'YSc7IHNlbGVjdCBzbGVlcCg0KTsgLS0g==' #"a'; select sleep(4); -- "
        self.url = self.utility.api_login_url # ex: http://127.0.0.1/

    def __str__(self):
        return '%s object (target: %s, description: %s)' % (self.name, self.url, self.description)

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
            "session_id": "",
            "point" : 0.0
        }

        #=======================================================================
        # User1 registration and login
        #=======================================================================

        # User1 registration
        session1 = self.utility.create_http_session()
        user_id1, password1, nick_name1 = self.utility.user_registration(session1)

        #utility.print_message(self.utility.none, 'user_id: %s, pass: %s, name: %s' % (user_id1, password1, nick_name1))

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
        
        # User Login
        session_id = self.utility.user_login(session1, user_id1, password1)
        if session_id == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: user1 login failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "user1 registration OK but login failed normally."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user1 login OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "user1 registration and login OK."
            return_values["session_id"] = session_id
        

        #=======================================================================
        # User2 registration and SQLi test
        #=======================================================================

        data = base64.b64decode(self.b64data).decode('utf-8')

        # User2 registration
        session2 = self.utility.create_http_session()

        start = time.time()
        res1 = self.utility.user_registration_sqli(session2, data)
        end = time.time()
        elapsed = end - start
        #self.utility.print_message(self.utility.note, '%s: elapsed time: %s' % (self.name, elapsed))
        if res1 != None:
            if elapsed >= 4:
                # SQLi detected
                if self.debug:
                    self.utility.print_message(self.utility.fail, '%s: Create User NG and SQLi sleep(4) detected(target: %s, elapsed time: %s)' % (self.name, self.url, elapsed))
                return_values["description"] = "SQLi detected."
                return_values["result"] = False
                return return_values
            else:
                # SQLi not detected
                if self.debug:
                    self.utility.print_message(self.utility.note, '%s: Create User OK and also SQLi sleep(4) not detected(target: %s, elapsed time: %s)' % (self.name, self.url, elapsed))
                return_values["description"] = "SQLi not detected."
                return_values["result"] = True
                return_values["point"] = self.point
                return return_values
        else:
            # SQLi request failed but creating user user1 was successful
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: Create User NG and SQLi test failed(target: %s, elapsed time: %s)' % (self.name, self.url, elapsed))
            return_values["description"] = "SQLi request failed but creating user user1 was successful."
            return_values["result"] = True
            return_values["point"] = self.point
            return return_values


