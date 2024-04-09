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
        config.read(os.path.join(full_path, 'crawler_config.ini'), encoding='utf-8')

        try:
            db_path = os.path.join(full_path, config['DB']['db_path'])
            os.makedirs(db_path, exist_ok=True)
            self.db_file = os.path.join(db_path, config['DB']['db_file'].format(utility.team_name))
            self.con_timeout = int(config['DB']['con_timeout'])
            self.isolation_level = config['DB']['isolation_level']

            # Create or connect to database.
            self.conn = None
            if os.path.exists(self.db_file) is False:
                # Create table.
                self.db_initialize('user_info')
                self.db_initialize('game_status')
            else:
                # Create connection.
                self.conn = sqlite3.connect(self.db_file, timeout=self.con_timeout, isolation_level=self.isolation_level)
        except Exception as e:
            self.utility.print_message(FAIL, f'Reading crawler_config.ini is failure : {e}')
            sys.exit(1)

        # Query templates.
        self.state_select = 'SELECT * FROM UserInfoTBL WHERE status = ?'
        self.state_select_id = 'SELECT id FROM UserInfoTBL WHERE user_id = ?'
        self.state_select_injustice = 'SELECT injustice_num FROM UserInfoTBL WHERE user_id = ?'
        self.state_select_charge = 'SELECT sum(charge) FROM UserInfoTBL'
        self.state_select_game_status = 'SELECT * FROM GameStatusTBL WHERE learner_name = ? AND epoch = ?'
        self.state_insert = 'INSERT INTO UserInfoTBL (status,user_id,password,nickname, charge,injustice_num) VALUES (?,?,?,?,0,0)'
        self.state_insert_game_status = 'INSERT INTO GameStatusTBL (learner_name,epoch,charge_amount,error,error_reason,is_cheat,registration_date) VALUES (?,?,?,?,?,?,?)'
        self.state_update_inactive = 'UPDATE UserInfoTBL SET status = 0 WHERE user_id = ?'
        self.state_update_charge = 'UPDATE UserInfoTBL SET charge = ? WHERE user_id = ?'
        self.state_update_injustice_num = 'UPDATE UserInfoTBL SET injustice_num = ? WHERE user_id = ?'
        self.state_update_all = 'UPDATE UserInfoTBL ' \
                                'SET ' \
                                'created_at = ?,' \
                                'level = ?,'\
                                'exp = ?,'\
                                'gold = ?,' \
                                'max_hp = ?,' \
                                'max_stamina = ?,' \
                                'max_str = ?,' \
                                'need_exp = ?,' \
                                'stamina = ?,'\
                                'staminaupdated_at = ?,'\
                                'weapon_id = ?,'\
                                'armor_id = ? '\
                                'WHERE user_id = ?'
        self.state_delete_user_info = 'DELETE FROM UserInfoTBL WHERE user_id = ?'
        self.state_delete_all_user_info = 'DELETE FROM UserInfoTBL'
        self.state_delete_all_operating_ratio = 'DELETE FROM GameStatusTBL'

    # Initialize Data base.
    def db_initialize(self, table_name):
        with sqlite3.connect(self.db_file, timeout=self.con_timeout, isolation_level=self.isolation_level) as conn:
            if table_name == 'user_info':
                try:
                    # Create table.
                    sql_query = 'CREATE TABLE IF NOT EXISTS UserInfoTBL(' \
                                'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                                'status INTEGER, ' \
                                'charge INTEGER, ' \
                                'injustice_num INTEGER, ' \
                                'user_id TEXT, ' \
                                'password TEXT, '\
                                'nickname TEXT, '\
                                'created_at TEXT, '\
                                'level INTEGER, '\
                                'exp INTEGER, '\
                                'gold INTEGER, ' \
                                'max_hp INTEGER, ' \
                                'max_stamina INTEGER, ' \
                                'max_str INTEGER, ' \
                                'need_exp INTEGER, ' \
                                'stamina INTEGER, '\
                                'staminaupdated_at TEXT, '\
                                'weapon_id INTEGER, '\
                                'armor_id INTEGER);'
                    conn.execute('begin transaction')
                    conn.execute(sql_query)
                    conn.commit()
                    self.conn = conn
                except Exception as e:
                    self.utility.print_message(FAIL, 'Could not create {} table: {}'.format(table_name, sql_query))
                    self.utility.print_exception(e, '')
                    sys.exit(1)
            elif table_name == 'game_status':
                sql_query = ''
                try:
                    # Create table.
                    sql_query = 'CREATE TABLE IF NOT EXISTS GameStatusTBL(' \
                                'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                                'learner_name, ' \
                                'epoch INTEGER, ' \
                                'charge_amount, ' \
                                'error INTEGER, ' \
                                'error_reason INTEGER, ' \
                                'is_cheat INTEGER, ' \
                                'registration_date DATE);'
                    conn.execute('begin transaction')
                    conn.execute(sql_query)
                    conn.commit()
                    self.conn = conn
                except Exception as e:
                    self.utility.print_message(FAIL, 'Could not create {} table: {}'.format(table_name, sql_query))
                    self.utility.print_exception(e, '')
                    sys.exit(1)
            else:
                self.utility.print_message(FAIL, 'Indicator {} is unknown.'.format(table_name))
                sys.exit(1)

    # Execute INSERT query.
    def insert(self, conn, sql_query, params):
        conn.execute('begin transaction')
        conn.execute(sql_query, params)
        conn.commit()

    # Execute UPDATE query.
    def update(self, conn, sql_query, params):
        conn.execute('begin transaction')
        conn.execute(sql_query, params)
        conn.commit()

    # Execute DELETE query.
    def delete(self, conn, sql_query, params=()):
        conn.execute('begin transaction')
        conn.execute(sql_query, params)
        conn.commit()

    # Execute SELECT query.
    def select(self, conn, sql_query, params=()):
        cursor = conn.cursor()
        cursor.execute(sql_query, params)
        return cursor
