#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CheckPlayerInfo(object):
    def __init__(self, utility, host="127.0.0.1", path="/", debug=False):
        self.utility = utility
        self.utility.target = host
        self.point = float(self.utility.point_playerinfo)
        self.host = host
        self.path = path
        self.debug = debug
        self.description = "The module can check if the web application is currently working and also check the player information inpersonate."
        self.url = self.utility.api_pinfo_url # ex: http://127.0.0.1


    def __str__(self):
        return 'CheckPlayer object (target: %s, description: %s)' % (self.url, self.description)

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

        #utility.print_message(utility.none, 'user_id: %s, pass: %s, name: %s' % (user_id1, password1, nick_name1))

        if user_id1 == None or password1 == None or nick_name1 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, 'CheckPlayer: user1 registration failed(target: %s)' % (self.url))
            return_values["description"] = "user1 registration failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, 'CheckPlayer: user1 registration OK(target: %s)' % (self.url))
            return_values["user_id"] = user_id1
            return_values["password"] = password1
            return_values["nick_name"] = nick_name1
        
        # User1 Login
        session_id1 = self.utility.user_login(session1, user_id1, password1)
        if session_id1 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, 'CheckPlayer: user1 login failed(target: %s)' % (self.url))
            return_values["description"] = "user1 registration OK but login failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, 'CheckPlayer: user1 login OK(target: %s)' % (self.url))
            return_values["description"] = "user1 registration and login OK."
            return_values["session_id"] = session_id1
        
        # Get Player Information for User1
        res1 = self.utility.get_player_info(session1)
        #utility.print_message(utility.warning, 'res1: %s' % (res1))
        id1 = res1["id"]
        cookie_domain = session1.cookies.list_domains()[0]

        # for debug
        #utility.print_message(utility.warning, 'session1: %s' % (vars(session1)))
        #session1.cookies.set('user_data', "1", domain=cookie_domain, path='/')
        #utility.print_message(utility.warning, 'session1: %s' % (vars(session1)))
        
        
        #=======================================================================
        # User2 registration and login
        #=======================================================================

        # User2 registration
        session2 = self.utility.create_http_session()
        user_id2, password2, nick_name2 = self.utility.user_registration(session2)

        #utility.print_message(utility.none, 'user_id: %s, pass: %s, name: %s' % (user_id2, password2, nick_name2))

        if user_id2 == None or password2 == None or nick_name2 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, 'CheckPlayer: user2 registration failed(target: %s)' % (self.url))
            return_values["description"] = "user2 registration failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, 'CheckPlayer: user2 registration OK(target: %s)' % (self.url))
            return_values["user_id"] = user_id1
            return_values["password"] = password1
            return_values["nick_name"] = nick_name1
        
        # User2 Login
        session_id2 = self.utility.user_login(session2, user_id2, password2)
        if session_id2 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, 'CheckPlayer: user2 login failed(target: %s)' % (self.url))
            return_values["description"] = "user2 registration OK but login failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, 'CheckPlayer: user2 login OK(target: %s)' % (self.url))
            return_values["description"] = "user2 registration and login OK."
            return_values["session_id"] = session_id2
        
        # Get Player Information for User2
        res2 = self.utility.get_player_info(session2)
        id2 = res2["id"]

        if id1 == id2:
            if self.debug:
                self.utility.print_message(self.utility.fail, 'CheckPlayer: user1 and user2 have the same id(target: %s)' % (self.url))
            return_values["description"] = "user1 and user2 have the same id so maybe the application is not working properly."
            return_values["result"] = False
            return return_values
        
        # Set other user's id on cookie 'user_data'
        session2.cookies.set('user_data', str(id1), domain=cookie_domain, path='/')
        res3 = self.utility.get_player_info(session2)

        if res3["id"] == id1:
            if self.debug:
                self.utility.print_message(self.utility.note, 'CheckPlayer: user2 can get user1 information(target: %s)' % (self.url))
            return_values["description"] = "user2 can get user1 information."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.fail, 'CheckPlayer: user2 can not get user1 information(target: %s)' % (self.url))
            return_values["description"] = "user2 can not get user1 information."
            return_values["result"] = True
            return_values["point"] = self.point
            return return_values




