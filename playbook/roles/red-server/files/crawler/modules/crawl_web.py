#!/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import re

# Printing colors.
OK_BLUE = '\033[94m'      # [*]
NOTE_GREEN = '\033[92m'   # [+]
FAIL_RED = '\033[91m'     # [-]
WARN_YELLOW = '\033[93m'  # [!]
ENDC = '\033[0m'
PRINT_OK = OK_BLUE + '[*]' + ENDC
PRINT_NOTE = NOTE_GREEN + '[+]' + ENDC
PRINT_FAIL = FAIL_RED + '[-]' + ENDC
PRINT_WARN = WARN_YELLOW + '[!]' + ENDC

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Utility class.
class Crawl_Web:
    def __init__(self, utility):
        self.utility = utility

        # Read config.ini.
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.join(self.full_path, '../')

    # Execute crawling.
    def execute_crawling(self, session, team, site_type, target_url, score, keywords):
        self.utility.print_message(NOTE, 'Users are crawling on the {} site.'.format(site_type))

        ret_status = True

        # Get top page response.
        status, response = self.utility.send_request(session, 'get', target_url, self.utility.http_req_header, {})

        # Check response.
        if status is False or\
                self.utility.judge_hacked(response, self.utility.regex_hacked) is False or\
                self.utility.judge_hacked(response, self.utility.regex_warning) is False:
            self.utility.print_message(FAIL, 'Can not continue the web crawling.')
            ret_status = False
            return ret_status
        else:
            ret_status = False
            for keyword in keywords:
                found_keywords = re.findall(keyword, response, flags=re.IGNORECASE)
                if len(found_keywords) != 0:
                    ret_status = True
                    self.utility.print_message(OK, 'Found default keyword: {}.'.format(found_keywords))
                    break

        # Send score to score server.
        if ret_status:
            self.utility.print_message(OK, 'Accessing to : {}.'.format(target_url))
            if self.utility.send_score(team, site_type, score):
                self.utility.print_message(OK, 'Successful sending score.')
            else:
                self.utility.print_message(FAIL, 'Failure sending score.')
        else:
            self.utility.print_message(WARNING, 'Not found default keywords: {}.'.format(target_url))

        return ret_status
