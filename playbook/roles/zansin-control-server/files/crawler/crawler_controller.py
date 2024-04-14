#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import codecs
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from .util import Utilty
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


# Execute crawling of Game.
def play_game(utility, learner_name, start_time, end_time):
    # Get all existing player's data from local db.
    player_list = []
    try:
        players = utility.get_all_players()
        for player_data in players:
            # Execute Login using credential in the DB.
            session = utility.create_http_session()
            session_id = utility.user_login(session, player_data['user_id'], player_data['password'])
            if session_id is None:
                # Inactive player that could not login.
                utility.print_message(WARNING, f'Player \"{player_data["user_id"]}\" is not active.')
                utility.update_user_status(player_data['user_id'])
                continue
            else:
                # Add active player to the player's list.
                exist_player = Player(utility, session, session_id, existing_player_data=player_data)
                player_list.append(exist_player)
    except Exception as e:
        utility.print_message(FAIL, f'Could not get player list from local db: {e.args}')

    # Execute crawling.
    player = None
    epochs = 1
    now_date = datetime.now()
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

        # Judgement of cheat users.
        count_cheat_user_in_ranking = 0
        nick_names_in_crawler = [player.nick_name for player in player_list]

        # Check cheat: If there are high level users in the level ranking that has not been registered by the crawler.
        is_cheat = False
        cheat_reason = ''
        try:
            response, _, _ = utility.get_ranking(utility.create_http_session())
            if response is not None:
                level_ranking_user_names_out_of_crawler = set()
                level_ranking_user_names_out_of_crawler.update(
                    [d['nick_name'] for d in response if d['nick_name'] not in nick_names_in_crawler])
                count_cheat_user_in_ranking += len(level_ranking_user_names_out_of_crawler)
                utility.print_message(NOTE, f'The number of level cheat users: {len(level_ranking_user_names_out_of_crawler)}')
                cheat_reason = 'Level cheating occurred. ' if len(level_ranking_user_names_out_of_crawler) != 0 else ''

            # Consider level-1 users created not by the crawler in the weapon ranking as cheaters
            response, _, _ = utility.get_ranking(utility.create_http_session(), sort='weapon')
            if response is not None:
                weapon_ranking_user_names_out_of_crawler = set()
                weapon_ranking_user_names_out_of_crawler.update(
                    [d['nick_name']
                     for d in response
                     if d['level'] == 1 and d['nick_name'] not in nick_names_in_crawler])
                count_cheat_user_in_ranking += len(weapon_ranking_user_names_out_of_crawler)
                utility.print_message(NOTE, f'The number of gatya cheat users: {len(weapon_ranking_user_names_out_of_crawler)}')
                cheat_reason += 'Gatya cheat occurred.' if len(weapon_ranking_user_names_out_of_crawler) != 0 else ''

            # Judge cheat.
            is_cheat = True if count_cheat_user_in_ranking != 0 else False
        except Exception as e:
            time.sleep(10)
            utility.print_message(FAIL, f'Could not compute cheat user number: {e.args}.')

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
        utility.print_message(NOTE, f'Epoch {epochs}: {learner_name} End Game!!')
        time.sleep(waiting_time / utility.loop_delay_rate)
        epochs += 1


# Get judge result of crawler.
def get_judge_crawler_result(learner_name):
    utility = Utilty(learner_name, '', '')
    utility.sql = DbControl(utility)
    return utility.get_operation_ratio(learner_name)


# main.
def crawler_execution(learner_name, target_hostname, start_time, end_time, user_agent):
    # Create Utility instance.
    utility = Utilty(learner_name, target_hostname, user_agent)

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
