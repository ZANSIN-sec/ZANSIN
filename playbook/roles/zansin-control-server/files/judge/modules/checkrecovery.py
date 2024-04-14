#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CheckRecovery(object):
    def __init__(self, utility, host="127.0.0.1", path="/", debug=False):
        self.utility = utility
        self.utility.target = host
        self.point = float(self.utility.point_recoverycheat)
        self.name = 'CheckRecovery'
        self.host = host
        self.path = path
        self.debug = debug
        self.description = "The module can check if the web application is currently working and also check if someone can cheat at the Recovery function."
        self.charge = 1000
        self.url = self.utility.api_recovery_url # ex: http://127.0.0.1/


    def __str__(self):
        return '%s object (target: %s, description: %s)' % (self.name, self.url, self.description)

    __repr__ = __str__

    def test(self):
        recovery = False
  
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

        #self.utility.print_message(self.utility.none, 'user_id: %s, pass: %s, name: %s' % (user_id1, password1, nick_name1))

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


        # check own player information1
        pinfo01 = self.utility.get_player_info(session1)
        if pinfo01 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values
        
        old_gold = pinfo01["gold"]

        # Charge money
        charge01 = self.utility.charge_gold(session1, self.charge)
        if charge01 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: charge request failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login OK but charge request failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: charge request OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge request OK."


        # check own player information1-1
        pinfo01 = self.utility.get_player_info(session1)
        #self.utility.print_message(self.utility.none, 'pinfo01: %s' % pinfo01)
        if pinfo01 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values
        
        # check current ammount of gold
        new_gold = pinfo01["gold"]
        if new_gold != old_gold + self.charge:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: charge failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login OK but charge failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: charge OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK."
            old_gold = new_gold

        #=======================================================================
        # Correct pattern
        #=======================================================================

        # Do the Recovery
        recovery01 = self.utility.recovery_stamina(session1, 100)
        if recovery01 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: recovery request failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK, but recovery request is fail."
            recovery = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: recovery request OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge, recovery request OK."
            recovery = True

        # check own player information1-2
        pinfo01 = self.utility.get_player_info(session1)
        #self.utility.print_message(self.utility.none, 'pinfo01: %s' % pinfo01)
        if pinfo01 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values

        # check current ammount of gold. it expects to be the same as (before - 100)
        new_gold = pinfo01["gold"]
        if recovery and new_gold == old_gold - 100:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: Recovery did succeeded(target: %s)' % (self.name, self.url))
            return_values["description"] = "Recovery succeeded."
            old_gold = new_gold
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: Recovery did not succeeded(target: %s)' % (self.name, self.url))
            return_values["description"] = "Recovery was not succeeded."
            return_values["result"] = False
            return return_values
        recovery = False


        #=======================================================================
        # Wrong pattern 1: Zero-cost Recovery cheat
        #=======================================================================
        #=======================================================================
        # User2 registration and login
        #=======================================================================

        # User2 registration
        session2 = self.utility.create_http_session()
        user_id2, password2, nick_name2 = self.utility.user_registration(session2)

        #self.utility.print_message(self.utility.none, 'user_id: %s, pass: %s, name: %s' % (user_id2, password2, nick_name2))

        if user_id2 == None or password2 == None or nick_name2 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: user2 registration failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "user2 registration failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user2 registration OK(target: %s)' % (self.name, self.url))
            return_values["user_id"] = user_id2
            return_values["password"] = password2
            return_values["nick_name"] = nick_name2
        
        # User Login
        session_id = self.utility.user_login(session2, user_id2, password2)
        if session_id == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: user2 login failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "user2 registration OK but login failed normally."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user2 login OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "user2 registration and login OK."
            return_values["session_id"] = session_id


        # check own player information2-1
        pinfo02 = self.utility.get_player_info(session2)
        if pinfo02 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values
        
        old_gold = pinfo02["gold"]

        # Charge money
        charge02 = self.utility.charge_gold(session2, self.charge)
        if charge02 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: charge request failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login OK but charge request failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: charge request OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge request OK."


        # check own player information2-2
        pinfo02 = self.utility.get_player_info(session2)
        if pinfo02 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values
        
        # check current ammount of gold
        new_gold = pinfo02["gold"]
        if new_gold != old_gold + self.charge:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: charge failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login OK but charge failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: charge OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK."
            old_gold = new_gold


        # Do the Recovery: cost 0
        recovery02 = self.utility.recovery_stamina(session2, 0)
        if recovery02 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: recovery 0 request failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK, Zero-cost recovery cheat is fail."
            recovery = False
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: recovery 0 request OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK, but Zero-cost recovery cheat is maybe found."
            recovery = True

        # check own player information2-3
        pinfo02 = self.utility.get_player_info(session2)
        if pinfo02 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values

        # check current ammount of gold. it expects to be the same as before
        new_gold = pinfo02["gold"]
        #print("new_gold: %s, old_gold: %s" % (newRecovery, old_gold))
        if recovery and new_gold == old_gold:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: Zero-cost Recovery cheat was found(target: %s, new: %s, old: %s)' % (self.name, self.url, new_gold, old_gold))
            return_values["description"] = "Zero-cost Recovery cheat was found."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: Zero-cost Recovery cheat was not found(target: %s, new: %s, old: %s)' % (self.name, self.url, new_gold, old_gold))
            return_values["description"] = "Zero-cost Recovery cheat was not found."
        recovery = False
        old_gold = new_gold






        #=======================================================================
        # Wrong pattern 2: Cost 1 gold Recovery cheat 
        #=======================================================================
        #=======================================================================
        # User3 registration and login
        #=======================================================================

        # User3 registration
        session3 = self.utility.create_http_session()
        user_id3, password3, nick_name3 = self.utility.user_registration(session3)

        #self.utility.print_message(self.utility.none, 'user_id: %s, pass: %s, name: %s' % (user_id3, password3, nick_name3))

        if user_id3 == None or password3 == None or nick_name3 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: user3 registration failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "user3 registration failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user3 registration OK(target: %s)' % (self.name, self.url))
            return_values["user_id"] = user_id3
            return_values["password"] = password3
            return_values["nick_name"] = nick_name3
        
        # User Login
        session_id = self.utility.user_login(session3, user_id3, password3)
        if session_id == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: user3 login failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "user3 registration OK but login failed normally."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user3 login OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "user3 registration and login OK."
            return_values["session_id"] = session_id


        # check own player information3-1
        pinfo03 = self.utility.get_player_info(session3)
        if pinfo03 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values
        
        old_gold = pinfo03["gold"]

        # Charge money
        charge03 = self.utility.charge_gold(session3, self.charge)
        if charge03 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: charge request failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login OK but charge request failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: charge request OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge request OK."


        # check own player information3-2
        pinfo03 = self.utility.get_player_info(session3)
        if pinfo03 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values
        
        # check current ammount of gold
        new_gold = pinfo03["gold"]
        if new_gold != old_gold + self.charge:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: charge failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login OK but charge failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: charge OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK."
            old_gold = new_gold


        # Do the Recovery: cost 1
        recovery03 = self.utility.recovery_stamina(session3, 1)
        if recovery03 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: recovery 1 request failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but recovery cost 1 failed."
            recovery = False
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: recovery 1 request OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login, charge and recovery cost 1 OK."
            recovery = True

        # check own player information3-3
        pinfo03 = self.utility.get_player_info(session3)
        if pinfo03 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values

        # check current ammount of gold. it expects to be the same as (before - 1)
        new_gold = pinfo03["gold"]
        #print("new_gold: %s, old_gold: %s" % (new_gold, old_gold))
        if recovery and new_gold == old_gold - 1:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: Cost 1 gold Recovery cheat was found(target: %s, new: %s, old: %s)' % (self.name, self.url, new_gold, old_gold))
            return_values["description"] = "Cost 1 gold Recovery cheat was found."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: Cost 1 gold Recovery cheat was not found(target: %s, new: %s, old: %s)' % (self.name, self.url, new_gold, old_gold))
            return_values["description"] = "Cost 1 gold Recovery cheat was not found."
            return_values["result"] = True
            return_values["point"] = self.point
            return return_values

