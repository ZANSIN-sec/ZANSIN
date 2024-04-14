#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CheckBattle(object):
    def __init__(self, utility, host="127.0.0.1", path="/", debug=False):
        self.utility = utility
        self.utility.target = host
        self.point = float(self.utility.point_battlecheat)
        self.name = 'CheckBattle'
        self.host = host
        self.path = path
        self.debug = debug
        self.description = "The module can check if the web application is currently working and also check if someone can cheat at the Battle function."
        self.battle_url = self.utility.api_battle_url # ex: http://127.0.0.1/
        self.courseget_url = self.utility.api_courseget_url # ex: http://127.0.0.1/
        self.courseset_url = self.utility.api_courseset_url # ex: http://127.0.0.1/
        self.walkthrue = False # for testing only. if you need to test for full function, please set True.


    def __str__(self):
        return '%s object (target: %s, description: %s)' % (self.name, self.battle_url, self.description)

    __repr__ = __str__

    def test(self):
  
        return_values = {
            "host": self.host,
            "url": self.battle_url,
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
                self.utility.print_message(self.utility.fail, '%s: user1 registration failed(target: %s)' % (self.name, self.battle_url))
            return_values["description"] = "user1 registration failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user1 registration OK(target: %s)' % (self.name, self.battle_url))
            return_values["user_id"] = user_id1
            return_values["password"] = password1
            return_values["nick_name"] = nick_name1
        
        # User1 Login
        session_id1 = self.utility.user_login(session1, user_id1, password1)
        if session_id1 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: user1 login failed(target: %s)' % (self.name, self.battle_url))
            return_values["description"] = "user1 registration OK but login failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user1 login OK(target: %s)' % (self.name, self.battle_url))
            return_values["description"] = "user1 registration and login OK."
            return_values["session_id"] = session_id1
        
        # Get Player Information for User1
        res11 = self.utility.get_player_info(session1)
        #utility.print_message(utility.warning, 'res1: %s' % (res1))
        id1 = res11["id"]



        #=======================================================================
        # Get Course Information
        #=======================================================================
        course = self.utility.get_course(session1)
        if course == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: The CourseGet API is not working properly(target: %s)' % (self.name, self.courseget_url))
            return_values["description"] = "The CourseSet API is not working properly."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: The CourseGet API is OK(target: %s)' % (self.name, self.courseget_url))
            return_values["description"] = "The CourseGet API is working properly."

        #=======================================================================
        # Check Course Information
        #=======================================================================
        #self.utility.print_message(self.utility.none, 'course: %s' % (course))
        battle_info = self.utility.set_course(session1, 1)
        if battle_info["course"] != 1:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: The CourseSet API is not working properly(target: %s)' % (self.name, self.courseset_url))
            return_values["description"] = "The CourseSet API is not working properly."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: The CourseSet API is OK(target: %s)' % (self.name, self.courseset_url))
            return_values["description"] = "The Course APIs are working properly."

        #=======================================================================
        # Check debug function on the CourseSetAPI
        #=======================================================================
        #self.utility.print_message(self.utility.none, 'course: %s' % (course))
        for i in range(0, len(course)):
            if course[i]["id"] == 6:
                battle_info = self.utility.set_course(session1, 6)
                #self.utility.print_message(self.utility.none, 'battle_info: %s' % (battle_info))
                if not battle_info == None and 'result' in battle_info.keys() and battle_info["result"] == "ok":
                    if self.debug:
                        self.utility.print_message(self.utility.fail, '%s: It still has a debug function(target: %s, %s)' % (self.name, self.courseget_url, self.courseset_url))
                    return_values["description"] = "The BattleAPI still has a debug function."
                    return_values["result"] = False
                    if self.walkthrue == False: # for testing
                        return return_values
                else:
                    if self.debug:
                        self.utility.print_message(self.utility.note, '%s: The CourseSet API is OK(target: %s)' % (self.name, self.courseset_url))
                    return_values["description"] = "The  BattleAPI is not has a debug function."
            else:
                if self.debug:
                    self.utility.print_message(self.utility.note, '%s: Course %s was found(target: %s).' % (self.name, course[i]["id"], self.courseset_url))
                        

        #=======================================================================
        # Set the Course and then access the BattleAPI normally.
        #=======================================================================
        battle_info = self.utility.set_course(session1, 1)
        if battle_info["course"] != 1:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: The CourseSet API is not working properly(target: %s)' % (self.name, self.courseset_url))
            return_values["description"] = "The CourseSet API is not working properly."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: Set Course 1 OK(target: %s)' % (self.name, self.courseset_url))
        
        response = self.utility.battle(session1, battle_info)
        #self.utility.print_message(self.utility.none, 'response: %s' % (response))

        if response == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: The Battle API was not working currently(target: %s)' % (self.name, self.battle_url))
            return_values["description"] = "The Battle API was not working currently."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: The Battle API was working currently(target: %s)' % (self.name, self.battle_url))


        #=======================================================================
        # Set the Course normally and do a cheat on the BattleAPI.
        #=======================================================================
        battle_info = self.utility.set_course(session1, 1)
        if battle_info["course"] != 1:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: The CourseSet API is not working properly(target: %s)' % (self.name, self.courseset_url))
            return_values["description"] = "The CourseSet API is not working properly."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: Set Course 1 OK(target: %s)' % (self.name, self.courseset_url))
        
        response = self.utility.cheat_battle(session1, battle_info)
        #self.utility.print_message(self.utility.none, 'response: %s' % (response))

        if response == None:
            # The cheat request failed and probably received an Error response
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: The cheat request failed and probably received an Error response(target: %s)' % (self.name, self.battle_url))
            return_values["description"] = "The Cheat was failed."
            return_values["result"] = True
            return_values["point"] = self.point
            return return_values
        else:
            if response["status"]["result"] == "win":
                if self.debug:
                    self.utility.print_message(self.utility.fail, '%s: The Cheat was Succeed(target: %s)' % (self.name, self.battle_url))
                return_values["description"] = "The BattleAPI still includes a cheat issue."
                return_values["result"] = False
                return return_values
            else:
                # The cheat request failed and received a normal response that was probably used from server-side data.
                if self.debug:
                    self.utility.print_message(self.utility.note, '%s: The cheat request failed and received a normal response that was probably use server-side data(target: %s)' % (self.name, self.battle_url))
                return_values["description"] = "The BattleAPI was probably use server-side data."
                return_values["result"] = True
                return_values["point"] = self.point
                return return_values





