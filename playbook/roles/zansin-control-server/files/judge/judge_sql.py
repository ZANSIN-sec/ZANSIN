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
            db_path = os.path.join(full_path, config['DB']['db_path'])
            os.makedirs(db_path, exist_ok=True)
            self.db_file = os.path.join(db_path, config['DB']['db_file'])
            self.con_timeout = int(config['DB']['con_timeout'])
            self.isolation_level = config['DB']['isolation_level']
            self.table_name_judge_attack = 'JudgeAttackTBL'

            # Create or connect to database.
            self.conn = None
            if os.path.exists(self.db_file) is False:
                # Create table.
                self.db_initialize('attack_judge')
            else:
                # Create connection.
                self.conn = self.create_db_connection(self.db_file)
        except Exception as e:
            self.utility.print_message(FAIL, f'Reading judge_config.ini is failure : {e}')
            sys.exit(1)

        # Query template.
        self.state_insert_judge_attack_result = f'INSERT INTO {self.table_name_judge_attack} ' \
                                                f'(technical_point, registration_date) VALUES (?,?)'
        self.state_select_judge_attack_result = f'SELECT technical_point FROM {self.table_name_judge_attack}' \
                                                f' ORDER BY id DESC LIMIT 1'

    # Initialize Data base.
    def db_initialize(self, table_name):
        with sqlite3.connect(self.db_file, timeout=self.con_timeout, isolation_level=self.isolation_level) as conn:
            if table_name == 'attack_judge':
                try:
                    # Create table.
                    sql_query = f'CREATE TABLE IF NOT EXISTS {self.table_name_judge_attack}(' \
                                f'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                                f'technical_point FLOAT, ' \
                                f'registration_date DATE);'
                    conn.execute('begin transaction')
                    conn.execute(sql_query)
                    conn.commit()
                    self.conn = conn
                except Exception as e:
                    self.utility.print_message(FAIL, f'Could not create {table_name} table: {sql_query}')
                    self.utility.print_exception(e, '')
                    sys.exit(1)

    # DB Connection.
    def create_db_connection(self, db_path):
        return sqlite3.connect(db_path, timeout=self.con_timeout, isolation_level=self.isolation_level)

    # Execute INSERT query.
    def insert(self, conn, sql_query, params):
        conn.execute('begin transaction')
        conn.execute(sql_query, params)
        conn.commit()

    # Execute SELECT query.
    def select(self, conn, sql_query, params=()):
        cursor = conn.cursor()
        cursor.execute(sql_query, params)
        return cursor