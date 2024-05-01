#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import codecs
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from .util import Utility
from .crawler_sql import DbControl
from .modules.player import Player
from .constants import *

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Display banner.
def show_banner(utility):
    banner = """
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
███████╗ █████╗ ███╗   ██╗███████╗██╗███╗   ██╗       ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗ 
╚══███╔╝██╔══██╗████╗  ██║██╔════╝██║████╗  ██║      ██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗
  ███╔╝ ███████║██╔██╗ ██║███████╗██║██╔██╗ ██║█████╗██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝
 ███╔╝  ██╔══██║██║╚██╗██║╚════██║██║██║╚██╗██║╚════╝██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗
███████╗██║  ██║██║ ╚████║███████║██║██║ ╚████║      ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═══╝       ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""" + 'by ' + os.path.basename(__file__)
    utility.print_message(NONE, banner)
    show_credit(utility)
    time.sleep(utility.banner_delay)


# Show credit.
def show_credit(utility):
    credit = u"""
       =[ Version : ZANSIN-Crawler v0.0.1       ]=
+ -- --=[ Author  : @bbr_bbq, @kazukiigeta      ]=--
+ -- --=[ https://github.com/ZANSIN-sec/ZANSIN/ ]=--
    """
    utility.print_message(NONE, credit)


def is_valid_training_time(start_time, end_time):
    return True if start_time <= end_time else False


def judge_cheat_users(utility, player_list):
    # Judgement of cheat users.
    count_cheat_user_in_ranking = 0
    cheat_reason = ''
    nick_names_in_crawler = [player.nick_name for player in player_list]

    try:
        # Helper function to filter and count cheat users.
        def count_and_document_cheat_users(response, condition=lambda d: True, message='cheat users'):
            if response is None:
                return 0
            cheat_users = {d['nick_name'] for d in response if condition(d)}
            cheat_count = len(cheat_users)
            if cheat_count:
                utility.print_message(NOTE, f'The number of {message}: {cheat_count}')
                return cheat_count
            return 0

        # Check level cheats.
        response, _, _ = utility.get_ranking(utility.create_http_session())
        level_cheat_condition = lambda d: (
                d['level'] == utility.level_cheat_level and
                d['stamina'] == utility.level_cheat_stamina and
                d['weapon_id'] == utility.level_cheat_weapon_id and d['armor_id'] == utility.level_cheat_armor_id and
                d['gold'] == utility.level_cheat_gold and
                d['exp'] == utility.level_cheat_exp
        )
        count_cheat_user_in_ranking += count_and_document_cheat_users(response,
                                                                      condition=level_cheat_condition,
                                                                      message='level cheat users')

        # Check battle cheats.
        response, _, _ = utility.get_ranking(utility.create_http_session(), sort='exp')
        battle_cheat_condition = lambda d: (
                d['nick_name'] not in nick_names_in_crawler and
                d['exp'] == utility.battle_cheat_exp
        )
        count_cheat_user_in_ranking += count_and_document_cheat_users(response,
                                                                      condition=battle_cheat_condition,
                                                                      message='battle cheat users')

        # Check gatya (weapon) cheats.
        response, _, _ = utility.get_ranking(utility.create_http_session(), sort='weapon')
        gatya_weapon_cheat_condition = lambda d: (
                d['nick_name'] not in nick_names_in_crawler and
                d['gold'] == utility.gatya_cheat_gold and
                d['level'] == utility.gatya_cheat_level and
                d['weapon_id'] in utility.gatya_cheat_weapon_id
        )
        count_cheat_user_in_ranking += count_and_document_cheat_users(response,
                                                                      condition=gatya_weapon_cheat_condition,
                                                                      message='gatya (weapon) cheat users')

        # Check gatya (armor) cheats.
        response, _, _ = utility.get_ranking(utility.create_http_session(), sort='armor')
        gatya_armor_cheat_condition = lambda d: (
                d['nick_name'] not in nick_names_in_crawler and
                d['gold'] == utility.gatya_cheat_gold and
                d['level'] == utility.gatya_cheat_level and
                d['armor_id'] in utility.gatya_cheat_armor_id
        )
        count_cheat_user_in_ranking += count_and_document_cheat_users(response,
                                                                      condition=gatya_armor_cheat_condition,
                                                                      message='gatya (armor) cheat users')

        # Construct the cheat reason message
        if count_cheat_user_in_ranking:
            cheat_reason = 'All or any of the level cheating, battle cheating, and gacha cheating.'

        # Judge cheat
        is_cheat = count_cheat_user_in_ranking != 0
        return is_cheat, cheat_reason, count_cheat_user_in_ranking
    except Exception as e:
        time.sleep(10)
        utility.print_message(FAIL, f'Could not compute cheat user number: {e.args}.')
        return False, f'Error occurred: {e.args[0]}'


# Execute crawling of Game.
def play_game(utility, learner_name, start_time, end_time):
    # Initialize.
    player_list, epochs, now_date = [], 1, datetime.now()

    # Execute crawling.
    while now_date < end_time:
        now_date = datetime.now()
        if now_date < start_time:
            msg = f'[Game] The start time has not come yet. now={now_date.strftime(utility.get_time_format())}, ' \
                  f'start={start_time.strftime(utility.get_time_format())}'
            utility.print_message(WARNING, msg)
            time.sleep(1.0)
            continue

        # Check users number.
        if len(player_list) >= utility.max_player_num:
            utility.print_message(WARNING, 'Already reached max user number.')
            utility.print_message(WARNING, 'Could not add new player.')
            time.sleep(1)
        else:
            # Execute new player's Registration.
            utility.print_message(NOTE, 'New player\'s registration.')
            session = utility.create_http_session()
            user_id, password, nick_name = utility.user_registration(session)
            if user_id is None:
                session = None

            # Execute Login.
            utility.print_message(NOTE, f'Player "{user_id}" login.')
            session_id = utility.user_login(session, user_id, password)
            if session_id is not None:
                # Create New player's instance.
                utility.print_message(OK, f'Complete creating new player: {user_id}')
                utility.insert_new_user(user_id, password, nick_name)
                utility.player_id = utility.get_player_id(user_id)
                new_player = Player(utility, session, session_id)
                if new_player.get_user_information(save=True) is not False:
                    player_list.append(new_player)

        # Check cheat occurred previous epoch.
        game_results = []
        if not utility.is_cheat_previous_epoch(learner_name, epochs - 1):
            # Play game!!
            utility.print_message(NOTE, f'Epoch {epochs}: Start Game!!')
            with ThreadPoolExecutor(max_workers=utility.max_player_num, thread_name_prefix='thread') as executor:
                for player in player_list:
                    game_results.append(executor.submit(player.play_game))
        else:
            # Skip game.
            utility.print_message(NOTE, 'Skip playing game because of cheating that occurred in the previous epoch.')

        # Judge cheat users.
        is_cheat, cheat_reason, cheat_user_count = judge_cheat_users(utility, player_list)

        # End game for 1 epoch.
        is_playing_game_disable = False
        successful_player_list = []
        total_injustice_count = 0
        for player, game_result in zip(player_list, game_results):
            # Withdrawal.
            if game_result.result() is False:
                # Interrupt.
                is_playing_game_disable = True
                utility.print_message(WARNING, f'Player "{player.user_name}" interrupts the game.')
            else:
                # Add player who successful of game.
                successful_player_list.append(player)

            # Update charge amount, injustice number and so on.
            utility.update_charge_amount(player.charge_sum, player.user_name)
            utility.update_injustice_num(player.injustice_num, player.user_name)
            utility.update_all(player)

            # Count the total amount of injustice number in all the players.
            if player.injustice_num > 0:
                total_injustice_count += player.injustice_num

        # Store the amount of charge and operation ratio.
        charge_amount_per_epoch = utility.get_player_charge_in_this_epoch(epochs, successful_player_list)
        if utility.insert_game_status_to_db(learner_name,
                                            epochs,
                                            is_cheat,
                                            cheat_reason,
                                            is_playing_game_disable,
                                            charge_amount_per_epoch):
            utility.print_message(OK, 'Successful stored operation ratio/charge to DB.')
        else:
            utility.print_message(FAIL, 'Failure store operation ratio/charge to DB.')

        # Compute loop delay time.
        waiting_time = utility.judge_waiting_time(player_list)
        waiting_time += utility.epoch_delay_time

        # Waiting per epoch.
        utility.print_message(OK, f'{waiting_time}[s] waiting.')
        utility.print_message(NOTE, f'Epoch {epochs}: Player num={len(player_list)}, Earned charge={charge_amount_per_epoch}.')
        utility.print_message(NOTE, f'Cheat users num={cheat_user_count}, Note={cheat_reason}')
        utility.print_message(NOTE, f'Epoch {epochs}: {learner_name} End Game!!')
        time.sleep(waiting_time / utility.loop_delay_rate)
        epochs += 1


# Get judge result of crawler.
def get_judge_crawler_result(learner_name):
    utility = Utility(learner_name, '', '')
    utility.sql = DbControl(utility)
    return utility.get_operation_ratio(learner_name)


# main.
def crawler_execution(learner_name, target_hostname, start_time, end_time, user_agent):
    # Create Utility instance.
    utility = Utility(learner_name, target_hostname, user_agent)

    # Initialize Database.
    sql = DbControl(utility)
    utility.sql = sql

    # Show banner.
    show_banner(utility)

    # Get competition term.
    if is_valid_training_time(start_time, end_time) is False:
        msg = f'Indicated competition time is invalid : not "start={utility.transform_date_string(start_time)} ' \
              f'<= end={utility.transform_date_string(end_time)}".'
        utility.print_message(FAIL, msg)
        return False

    # Initialize tables.
    utility.delete_user_info_table()
    utility.delete_operating_ratio_table()

    # Execute playing Game.
    utility.ua = user_agent
    play_game(utility, learner_name, start_time, end_time)
