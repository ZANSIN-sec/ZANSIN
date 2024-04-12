#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import base64


class CheckImageUpload(object):
    def __init__(self, utility, host="127.0.0.1", path="/", debug=False):
        self.utility = utility
        self.utility.target = host
        self.point = float(self.utility.point_imageupload)
        self.name = 'CheckImageUpload'
        self.host = host
        self.path = path
        self.debug = debug
        self.upload = '/upload'
        self.download = '/images/players/'
        self.description = "The module can check if the web application is currently working and also check upload php file on image uploder on the player information."
        self.phpcode = '<?php $b64 = base64_encode("AQ!@WSXZ"); echo "this is a test message " . $b64;'
        self.b64image = 'iVBORw0KGgoAAAANSUhEUgAAAAsAAAAKCAIAAADtkjPUAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAUSURBVChTY/hPCIyqQAWEVPz/DwBW9kjGXP/IgAAAAABJRU5ErkJggg==' # 1x1 pixel image
        self.file1 = '_1799999999.png'
        self.file2 = '_1799999998.php'
        self.url = self.utility.api_imgupload_url # ex: http://127.0.0.1/


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
        #utility.print_message(utility.none, 'user_id: %s, pass: %s, name: %s' % (user_id1, password1, nick_name1))

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
        
        # User1 Login
        session_id1 = self.utility.user_login(session1, user_id1, password1)
        if session_id1 == None:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: user1 login failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "user1 registration OK but login failed."
            return_values["result"] = False
            return return_values
        else:
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: user1 login OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "user1 registration and login OK."
            return_values["session_id"] = session_id1
        
        # Get Player Information for User1
        res11 = self.utility.get_player_info(session1)
        id1 = res11["id"]
        
        # Upload Image file normally
        file1 = str(id1) + self.file1
        res21 = self.utility.upload_player_image(session1, file1, self.b64image)
        if not res21 == None and res21["result"].lower() == "ok":
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: image upload OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "image upload OK."
        else:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: image upload failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "image upload failed."
            return_values["result"] = False
            return return_values
        
        # Download Image file and then check data
        res22 = self.utility.get_player_info(session1)
        img1 = res22["image"]
        status, res23 = self.utility.get_request(self.utility.request_schema + "://" + self.host + self.download + img1, session1)
        if status:
            if base64.b64encode(res23.content).decode('utf-8') != self.b64image:
                if self.debug:
                    self.utility.print_message(self.utility.note, '%s: image download NG(target: %s)' % (self.name, self.url))
                return_values["description"] = "Can't upload image. The uploaded image was modified."
                return_values["result"] = False
                return return_values
            else:
                if self.debug:
                    self.utility.print_message(self.utility.note, '%s: image download OK(target: %s)' % (self.name, self.url))
                return_values["description"] = "image download OK and also same data."
        else:
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: image download failed(target: %s)' % (self.name, self.url))
            return_values["description"] = "image download failed1."
            return_values["result"] = False
            return return_values

        # Upload PHP file
        file2 = str(id1) + self.file2
        b64phpcode = base64.b64encode((self.phpcode).encode('utf-8')).decode('utf-8')
        res31 = self.utility.upload_player_image(session1, file2, b64phpcode)
        if not res31 == None and res31["result"].lower() == "ok":
            # might be uploaded a PHP file
            if self.debug:
                self.utility.print_message(self.utility.note, '%s: PHP upload OK(target: %s)' % (self.name, self.url))
            return_values["description"] = "PHP upload OK."
            return_values["result"] = False
        else:
            # Can't upload PHP file
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: PHP upload failed1(target: %s)' % (self.name, self.url))
            return_values["description"] = "PHP upload failed."
            return_values["result"] = True
            return_values["point"] = self.point
            return return_values
        
        # Download PHP file and then check data
        res32 = self.utility.get_player_info(session1)
        img2 = res32["image"]
        status, res33 = self.utility.get_request(self.utility.request_schema + "://" + self.host + self.download + img2, session1)
        if status:
            if re.search(r'QVEhQFdTWFo=', res33.text) != None:
                if self.debug:
                    self.utility.print_message(self.utility.note, '%s: the keyword is found(target: %s)' % (self.name, self.url))
                return_values["description"] = "The uploaded PHP file was executed. imgurl: " + res33.url
                return_values["result"] = False
                return return_values
            else:
                # PHP code was not working
                if self.debug:
                    self.utility.print_message(self.utility.note, '%s: the keyword is not found(target: %s)' % (self.name, self.url))
                return_values["description"] = "The uploaded PHP file was not executed. imgurl: " + res33.url
                return_values["result"] = True
                return_values["point"] = self.point
                return return_values
        else:
            # Page not found
            if self.debug:
                self.utility.print_message(self.utility.fail, '%s: The PHP file was not uploaded(target: %s)' % (self.name, self.url))
            return_values["description"] = "PHP file was not uploaded."
            return_values["result"] = True
            return_values["point"] = self.point
            return return_values


