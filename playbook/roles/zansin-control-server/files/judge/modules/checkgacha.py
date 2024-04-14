#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import re
import base64


class CheckGacha(object):
    def __init__(self, utility, host="127.0.0.1", path="/", debug=False):
        self.utility = utility
        self.utility.target = host
        self.point = float(self.utility.point_gachacheat)
        self.name = 'CheckGacha'
        self.host = host
        self.path = path
        self.debug = debug
        self.description = "The module can check if the web application is currently working and also check if someone can cheat at the Gacha function."
        self.charge = 1000
        self.url = self.utility.api_gacha_url # ex: http://127.0.0.1/


    def __str__(self):
        return '%s object (target: %s, description: %s)' % (self.name, self.url, self.description)

    __repr__ = __str__

    def test(self):
        gacha = False
  
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
        res01 = self.utility.get_player_info(session1)
        if res01 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values
        
        old_gold = res01["gold"]

        # Charge money
        res0 = self.utility.charge_gold(session1, self.charge)
        if res0 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: charge request failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login OK but charge request failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: charge request OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge request OK."


        # check own player information1
        res01 = self.utility.get_player_info(session1)
        if res01 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values
        
        # check current ammount of gold
        new_gold = res01["gold"]
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

        # Do the Gacha
        res1 = self.utility.get_gacha(session1, 100)
        if res1 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: gacha request failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK, but gacha request is fail."
            gacha = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: gacha request OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge, gacha request OK."
            gacha = True

        # check own player information1
        res11 = self.utility.get_player_info(session1)
        if res11 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values

        # check current ammount of gold. it expects to be the same as (before - 100)
        new_gold = res11["gold"]
        if gacha and new_gold == old_gold - 100:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: Gacha did succeeded(target: %s)' % (self.name, self.url))
            return_values["description"] = "Gacha succeeded."
            old_gold = new_gold
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: Gacha did not succeeded(target: %s)' % (self.name, self.url))
            return_values["description"] = "Gacha was not succeeded."
            return_values["result"] = False
            return return_values
        gacha = False


        #=======================================================================
        # Wrong pattern 1: Zero-cost Gacha cheat
        #=======================================================================

        # Do the Gacha: cost 0
        res2 = self.utility.get_gacha(session1, 0)
        if res2 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: gacha 0 request failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK, Zero-cost gacha cheat is fail."
            gacha = False
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: gacha 0 request OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK, but Zero-cost gacha cheat is maybe found."
            gacha = True

        # check own player information1
        res21 = self.utility.get_player_info(session1)
        if res21 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values

        # check current ammount of gold. it expects to be the same as before
        new_gold = res21["gold"]
        #print("new_gold: %s, old_gold: %s" % (new_gold, old_gold))
        if gacha and new_gold == old_gold:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: Zero-cost Gacha cheat was found(target: %s, new: %s, old: %s, %s)' % (self.name, self.url, new_gold, old_gold, res2))
            return_values["description"] = "Zero-cost Gacha cheat was found."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: Zero-cost Gacha cheat was not found(target: %s, %s)' % (self.name, self.url, res2))
            return_values["description"] = "Zero-cost Gacha cheat was not found."
        gacha = False
        old_gold = new_gold

        #=======================================================================
        # Wrong pattern 2: Cost 1 gold Gacha cheat 
        #=======================================================================

        # Do the Gacha: cost 1
        res3 = self.utility.get_gacha(session1, 1)
        if res3 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: gacha 1 request failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but gacha cost 1 failed."
            gacha = False
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: gacha 1 request OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login, charge and gacha cost 1 OK."
            gacha = True

        # check own player information2
        res31 = self.utility.get_player_info(session1)
        if res31 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values

        # check current ammount of gold. it expects to be the same as (before - 1)
        new_gold = res31["gold"]
        #print("new_gold: %s, old_gold: %s" % (new_gold, old_gold))
        if gacha and new_gold == old_gold - 1:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: Cost 1 gold Gacha cheat was found(target: %s, new: %s, old: %s, %s)' % (self.name, self.url, new_gold, old_gold, res3))
            return_values["description"] = "Cost 1 gold Gacha cheat was found."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: Cost 1 gold Gacha cheat was not found(target: %s, %s)' % (self.name, self.url, res3))
            return_values["description"] = "Cost 1 gold Gacha cheat was not found."
        gacha = False
        old_gold = new_gold




        #=======================================================================
        # Wrong pattern 3: Cost -1 gold Gacha cheat 
        #=======================================================================

        # Do the Gacha: cost -1
        res4 = self.utility.get_gacha(session1, -1)
        if res4 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: gacha -1 request failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but gacha cost -1 failed."
            gacha = False
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: gacha -1 request OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "login, charge and gacha cost -1 OK."

        # check own player information3
        res41 = self.utility.get_player_info(session1)
        if res41 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: get player info failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "login and charge OK but get player info failed."
            return_values["result"] = False
            return return_values

        # check current ammount of gold. it expects to be the same as (before + 1)
        new_gold = res41["gold"]
        #print("new_gold: %s, old_gold: %s" % (new_gold, old_gold))
        if gacha and new_gold == old_gold + 1:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: Cost -1 gold Gacha cheat was found(target: %s, new: %s, old: %s, %s)' % (self.name, self.url, new_gold, old_gold, res4))
            return_values["description"] = "Cost -1 gold Gacha cheat was found."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: Cost -1 gold Gacha cheat was not found(target: %s, %s)' % (self.name, self.url, res4))
            return_values["description"] = "Cost -1 gold Gacha cheat was not found."
            return_values["result"] = True
            return_values["point"] = self.point
            return return_values
        



