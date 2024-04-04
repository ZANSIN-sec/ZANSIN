#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import codecs
import threading
from docopt import docopt
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from sql import DbControl
from util import Utilty
from modules.player import Player

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Display banner.
def show_banner(utility):
    banner = """
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

███╗   ███╗██╗███╗   ██╗██╗       ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗ 
████╗ ████║██║████╗  ██║██║      ██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗
██╔████╔██║██║██╔██╗ ██║██║█████╗██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝
██║╚██╔╝██║██║██║╚██╗██║██║╚════╝██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗
██║ ╚═╝ ██║██║██║ ╚████║██║      ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝       ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝ (v4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""" + 'by ' + os.path.basename(__file__)
    utility.print_message(NONE, banner)
    show_credit(utility)
    time.sleep(utility.banner_delay)


# Show credit.
def show_credit(utility):
    credit = u"""
       =[ Version : MINI-Crawler v0.2.0                  ]=
+ -- --=[ Author  : @bbr_bbq, @kazukiigeta               ]=--
+ -- --=[ https://github.com/minihardening/mini4-crawler ]=--
    """
    utility.print_message(NONE, credit)


# Define command option.
__doc__ = """{f}
usage:
    {f} -t <team> | --team=<team> [--delete-db] [--debug] [--english] [--game] [--corp] [--repo]
    {f} -h | --help
options:
    -t Require     : Playing team (e.g., team-a, team-b, ... , team-y, team-z).
    --delete-db    : Delete local db (sqlite3/minih_v4.db).
    --english      : Specify abroad event.
    --debug        : It is test mode.
    -h --help Show this help message and exit.
""".format(f=__file__)


def check_competition_time(start_time, busy_time, end_time):
    return True if start_time <= busy_time <= end_time else False


def get_time_format():
    return '%Y%m%d%H%M%S'


# Execute crawling of Game.
def play_game(utility, learner_name, start_time, busy_time, end_time):
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
                session = None
                utility.print_message(WARNING, 'Player "{}" is not active.'.format(player_data['user_id']))
                utility.update_user_status(player_data['user_id'])
            else:
                # Add active player to the player's list.
                exist_player = Player(utility, session, session_id)
                exist_player.utility.player_id = player_data['id']
                exist_player.charge_sum = player_data['charge']
                exist_player.injustice_num = player_data['injustice_num']
                exist_player.user_name = player_data['user_id']
                exist_player.password = player_data['password']
                exist_player.nick_name = player_data['nickname']
                exist_player.created_at = player_data['created_at']
                exist_player.level = player_data['level']
                exist_player.exp = player_data['exp']
                exist_player.gold = player_data['gold']
                exist_player.max_hp = player_data['max_hp']
                exist_player.max_stamina = player_data['max_stamina']
                exist_player.max_str = player_data['max_str']
                exist_player.need_exp = player_data['need_exp']
                exist_player.stamina = player_data['stamina']
                exist_player.staminaupdated_at = player_data['staminaupdated_at']
                exist_player.weapon_id = player_data['weapon_id']
                exist_player.armor_id = player_data['armor_id']
                player_list.append(exist_player)
    except Exception as e:
        utility.print_message(FAIL, 'Could not get player list from local db: {}'.format(e.args))

    # Execute crawling.
    busy_flag = False
    player = None
    epochs = 0
    now_date = datetime.now()
    access_status_repo = {}
    while now_date < end_time:
        now_date = datetime.now()
        if now_date < start_time:
            msg = '[Game] The start time has not come yet. now={}, start={}'.format(now_date.strftime(get_time_format()),
                                                                                    start_time.strftime(get_time_format()))
            utility.print_message(WARNING, msg)
            time.sleep(1.0)
            continue
        elif busy_flag is False and now_date >= busy_time:
            msg = '[Game] The busy time has come. now={}, busy={}'.format(now_date.strftime(get_time_format()),
                                                                          busy_time.strftime(get_time_format()))
            utility.print_message(WARNING, msg)
            utility.print_message(WARNING, 'Delay time will be cut in half.')
            utility.loop_delay_rate = utility.busy_period_rate
            busy_flag = True

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
            utility.print_message(NOTE, 'Player "{}" login.'.format(user_id))
            session_id = utility.user_login(session, user_id, password)
            if session_id is None:
                session = None
            else:
                # Create New player's instance.
                utility.print_message(OK, 'Complete creating new player: {}'.format(user_id))
                utility.insert_new_user(user_id, password, nick_name)
                utility.player_id = utility.get_player_id(user_id)
                new_player = Player(utility, session, session_id)
                if new_player.get_user_information(save=True) is not False:
                    player_list.append(new_player)

        # Play game!!
        game_results = []
        utility.print_message(NOTE, 'Epoch {}: Start Game!!'.format(epochs + 1))
        with ThreadPoolExecutor(max_workers=utility.max_player_num, thread_name_prefix='thread') as executor:
            for player in player_list:
                game_results.append(executor.submit(player.play_game))

        # Judgement of cheat users.
        count_cheat_user_in_ranking = 0
        user_names_in_crawler = [player.user_name for player in player_list]

        # Consider high level users created not by the crawler in the level ranking as cheaters
        try:
            response, _, _ = utility.get_ranking(utility.create_http_session())
            if response is not None:
                level_ranking_user_names_out_of_crawler = set()
                level_ranking_user_names_out_of_crawler.update(
                    [d['user_name'] for d in response if d['user_name'] not in user_names_in_crawler])
                count_cheat_user_in_ranking += len(level_ranking_user_names_out_of_crawler)
                utility.print_message(NOTE,
                                      f'The number of level cheat users: {len(level_ranking_user_names_out_of_crawler)}')

            # Consider level-1 users created not by the crawler in the weapon ranking as cheaters
            response, _, _ = utility.get_ranking(utility.create_http_session(), sort='weapon')
            if response is not None:
                weapon_ranking_user_names_out_of_crawler = set()
                weapon_ranking_user_names_out_of_crawler.update(
                    [d['user_name']
                     for d in response
                     if d['level'] == 1 and d['user_name'] not in user_names_in_crawler])
                count_cheat_user_in_ranking += len(weapon_ranking_user_names_out_of_crawler)
                utility.print_message(NOTE,
                                      f'The number of gatya cheat users: {len(weapon_ranking_user_names_out_of_crawler)}')
        except Exception as e:
            time.sleep(10)
            utility.print_message(FAIL, 'Could not compute cheat user number: {}.'.format(e.args))

        # End game for 1 epoch.
        successful_player_list = []
        total_injustice_count = 0
        for player, game_result in zip(player_list, game_results):
            # Withdrawal.
            if game_result.result() is False:
                # Interrupt.
                utility.print_message(WARNING, 'Player "{}" interrupts the game.'.format(player.user_name))
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

        # Send the amount of charge to score server.
        # total_charge_amount_in_this_epoch = utility.get_player_charge()
        total_charge_amount_in_this_epoch = utility.get_player_charge_in_this_epoch(epochs + 1, successful_player_list)
        if utility.store_score_to_db(learner_name, total_charge_amount_in_this_epoch):
            utility.print_message(OK, 'Successful sending charge.')
        else:
            utility.print_message(FAIL, 'Failure sending charge.')

        # Compute loop delay time.
        penalty_time = utility.penalty_time_coef * total_injustice_count + count_cheat_user_in_ranking * utility.cheat_penalty_time_coef
        waiting_time = utility.judge_waiting_time(player_list) + penalty_time
        waiting_time += utility.epoch_delay_time

        # Waiting per epoch.
        utility.print_message(OK, '{}[s] waiting. (including penalty {}[s])'.format(waiting_time, penalty_time))
        utility.print_message(NOTE,
                              'Epoch {}: Player num={}, Earned charge={}.'.format(epochs + 1, len(player_list),
                                                                                  total_charge_amount_in_this_epoch))
        utility.print_message(NOTE, 'Epoch {}: {} End Game!!'.format(epochs + 1, learner_name))
        utility.print_message(NOTE, 'Repo: {}'.format(access_status_repo))
        time.sleep(waiting_time / utility.loop_delay_rate)
        epochs += 1


# main.
def crawler_execution(learner_name, start_time, busy_time, end_time):
    # Create Utility instance.
    utility = Utilty(learner_name)

    # Initialize Database.
    sql = DbControl(utility)
    utility.sql = sql

    # Show banner.
    show_banner(utility)

    # Get competition term.
    now_date = datetime.now()
    start_time = utility.transform_date_object(start_time, get_time_format())
    busy_time = utility.transform_date_object(busy_time, get_time_format())
    end_time = utility.transform_date_object(end_time, get_time_format())
    if check_competition_time(start_time, busy_time, end_time) is False:
        msg = 'Indicated competition time is invalid : not "start={} <= busy={} <= end={}".'\
            .format(start_time, busy_time, end_time)
        utility.print_message(FAIL, msg)
        return False

    # Execute playing Game.
    play_game(utility, learner_name, start_time, busy_time, end_time)

