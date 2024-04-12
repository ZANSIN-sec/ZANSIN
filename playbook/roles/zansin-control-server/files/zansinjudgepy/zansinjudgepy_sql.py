#!/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import configparser
import sqlite3


# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Database control class.
class DbControl:
    def __init__(self, utility):
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.utility = utility

        # Read crawler_config.ini.
        full_path = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'judge_config.ini'), encoding='utf-8')

        try:
            self.con_timeout = int(config['DB']['con_timeout'])
            self.isolation_level = config['DB']['isolation_level']
        except Exception as e:
            self.utility.print_message(FAIL, f'Reading judge_config.ini is failure : {e}')
            sys.exit(1)

        # Query template.
        self.state_select_all_game_status = 'SELECT error FROM GameStatusTBL WHERE learner_name = ?'

    # DB Connection.
    def create_db_connection(self, db_path):
        return sqlite3.connect(db_path, timeout=self.con_timeout, isolation_level=self.isolation_level)

    # Execute SELECT query.
    def select(self, conn, sql_query, params=()):
        cursor = conn.cursor()
        cursor.execute(sql_query, params)
        return cursor
