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
from modules.crawl_web import Crawl_Web

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


# Check competition time.
def check_competition_time(start_time, lunch_time, restart_time, busy_time, end_time):
    if start_time < lunch_time < restart_time <= busy_time <= end_time:
        return True
    else:
        return False


# Execute crawling of corporate.
def run_crawling_corporate(utility, start_time, lunch_time, restart_time, busy_time, end_time):
    busy_flag = False
    now_date = datetime.now()
    access_status_corp = {}
    while now_date < end_time:
        now_date = datetime.now()
        if now_date < start_time:
            msg = '[Corp] The start time has not come yet. now={}, start={}'.format(now_date.strftime(time_format),
                                                                                    start_time.strftime(time_format))
            utility.print_message(WARNING, msg)
            time.sleep(1.0)
            continue
        elif lunch_time <= now_date < restart_time:
            msg = '[Corp] Now, lunch time. now={}, restart={}'.format(now_date.strftime(time_format),
                                                                      restart_time.strftime(time_format))
            utility.print_message(WARNING, msg)
            time.sleep(1.0)
            continue
        elif busy_flag is False and now_date >= busy_time:
            msg = '[Corp] The busy time has come. now={}, busy={}'.format(now_date.strftime(time_format),
                                                                          busy_time.strftime(time_format))
            utility.print_message(WARNING, msg)
            utility.print_message(WARNING, 'Delay time will be cut in half.')
            utility.loop_delay_rate_corporate = utility.busy_period_rate
            busy_flag = True

        web_crawling = Crawl_Web(utility)
        for category in utility.corp_categories:
            utility.print_message(NOTE, '[{}] Start Crawling.'.format(category))

            # Get Web site information.
            target_url, score, keywords = utility.get_web_info(category)

            # Crawling.
            if web_crawling.execute_crawling(utility.create_http_session(),
                                             opt_team,
                                             category,
                                             target_url,
                                             score,
                                             keywords):
                utility.print_message(NOTE, 'Successful accessing to {} site.'.format(category))
                access_status_corp[category] = True
            else:
                utility.print_message(FAIL, 'Failure accessing to {} site.'.format(category))
                access_status_corp[category] = False
            utility.print_message(NOTE, '[{}] End Crawling.'.format(category))

        utility.print_message(NOTE, 'Corp: {}'.format(access_status_corp))
        time.sleep(utility.corporate_delay_time / utility.loop_delay_rate_corporate)


# Execute crawling of Game.
def play_game(utility, start_time, lunch_time, restart_time, busy_time, end_time, is_repo=False):
    # Get repository file and store to local file.
    repo_hash_file = os.path.join(full_path, utility.repo_hash_file)
    if is_repo and os.path.exists(repo_hash_file) is False:
        status, _, hash_response = utility.get_repo_file(file_type='csv')
        if status is False:
            msg = 'Could not access to repository server: {}'.format(utility.repo_url_csv)
            utility.print_message(FAIL, msg)
            exit(1)
        with codecs.open(repo_hash_file, mode='w', encoding='utf-8') as fout:
            fout.write(hash_response)

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
            msg = '[Game] The start time has not come yet. now={}, start={}'.format(now_date.strftime(time_format),
                                                                                    start_time.strftime(time_format))
            utility.print_message(WARNING, msg)
            time.sleep(1.0)
            continue
        elif lunch_time <= now_date < restart_time:
            msg = '[Game] Now, lunch time. now={}, restart={}'.format(now_date.strftime(time_format),
                                                                      restart_time.strftime(time_format))
            utility.print_message(WARNING, msg)
            time.sleep(1.0)
            continue
        elif busy_flag is False and now_date >= busy_time:
            msg = '[Game] The busy time has come. now={}, busy={}'.format(now_date.strftime(time_format),
                                                                          busy_time.strftime(time_format))
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
        if utility.send_charge(opt_team, total_charge_amount_in_this_epoch):
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
        utility.print_message(NOTE, 'Epoch {}: {} End Game!!'.format(epochs + 1, opt_team))
        utility.print_message(NOTE, 'Repo: {}'.format(access_status_repo))
        time.sleep(waiting_time / utility.loop_delay_rate)
        epochs += 1

        # Checking status of repository server.
        if is_repo and epochs % utility.repo_interval == 0:
            # Check README.md.
            status, raw_res, _ = utility.get_repo_file(file_type='readme')
            if status is False:
                utility.print_message(WARNING, 'Could not access to repository server: {}'.format(
                    utility.repo_url_readme))
                access_status_repo['Readme'] = False
            elif utility.judge_hacked(raw_res, utility.repo_regex_hacked) is False:
                utility.print_message(WARNING, '{} is hacked!!'.format(utility.repo_url_readme))
                access_status_repo['Readme'] = False
            else:
                #  Send score to score server.
                access_status_repo['Readme'] = True
                if utility.send_score(opt_team, 'repository', utility.repo_score):
                    utility.print_message(OK, 'Successful sending score.')
                else:
                    utility.print_message(FAIL, 'Failure sending score.')

            # Check hash value of csv files (equipment.csv, level.csv).
            status, _, hash_remote = utility.get_repo_file(file_type='csv')
            if status is False:
                utility.print_message(WARNING,
                                      'Could not access to repository server: {}'.format(utility.repo_url_csv))
                access_status_repo['Csv'] = False
            else:
                # Open local hash file.
                with codecs.open(repo_hash_file, mode='r', encoding='utf-8') as fin:
                    hash_local = fin.read()

                # Compare local hash and remote hash.
                if hash_local != hash_remote:
                    utility.print_message(WARNING, 'Does not match the local hash "{}" and remote hash "{}".'.
                                          format(hash_local, hash_remote))
                    access_status_repo['Csv'] = False
                else:
                    #  Send score to score server.
                    access_status_repo['Csv'] = True
                    if utility.send_score(opt_team, 'repository', utility.repo_score):
                        utility.print_message(OK, 'Successful sending score.')
                    else:
                        utility.print_message(FAIL, 'Failure sending score.')


# main.
if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    full_path = os.path.dirname(os.path.abspath(__file__))

    # Get command argument.
    args = docopt(__doc__)
    opt_team = args['--team']
    opt_exec_game = args['--game']
    opt_exec_corp = args['--corp']
    opt_exec_repo = args['--repo']
    opt_delete_db = args['--delete-db']
    opt_debug = args['--debug']
    opt_english = args['--english']

    # Crawling all service (Game API, Repository, Corporate).
    if not opt_exec_game and not opt_exec_corp and not opt_exec_repo:
        opt_exec_game = True
        opt_exec_corp = True
        opt_exec_repo = True

    # Create Utility instance.
    utility = Utilty(opt_team, debug=opt_debug, english=opt_english)

    # Initialize Database.
    sql = DbControl(utility)
    utility.sql = sql

    # Delete local db (optional).
    if opt_delete_db:
        msg = 'The crawler will remove all user information from the local and server after 10 seconds!!'
        utility.print_message(WARNING, msg)
        time.sleep(10)

        # Get users to be removed from local DB
        player_list = []
        players = utility.get_all_players()

        for player_data in players:
            session = utility.create_http_session()
            session_id = utility.user_login(session, player_data['user_id'], player_data['password'])

            if session_id is None:
                # Inactive player that could not login.
                utility.print_message(FAIL, 'Login failed: user deletion need login')
                sys.exit()
            else:
                # Execute deletion of user
                exist_player = Player(utility, session, session_id)
                exist_player.delete_user(session)

        # Delete local DB of this crawler
        sql.delete(sql.conn, sql.state_delete_all)

    # Show banner.
    show_banner(utility)

    # Get competition term.
    now_date = datetime.now()
    time_format = '%Y%m%d%H%M%S'
    start_time = utility.transform_date_object(utility.competition_start_time, time_format)
    lunch_time = utility.transform_date_object(utility.competition_lunch_time, time_format)
    restart_time = utility.transform_date_object(utility.competition_restart_time, time_format)
    busy_time = utility.transform_date_object(utility.competition_busy_time, time_format)
    end_time = utility.transform_date_object(utility.competition_end_time, time_format)
    if check_competition_time(start_time, lunch_time, restart_time, busy_time, end_time) is False:
        msg = 'Indicated competition time is invalid : not "start={} < lunch={} < restart={} <= busy={} <= end={}".'\
            .format(start_time,
                    lunch_time,
                    restart_time,
                    busy_time,
                    end_time)
        utility.print_message(FAIL, msg)
        exit(1)

    # Execute crawling corporate.
    if opt_exec_corp:
        thread_corp = threading.Thread(target=run_crawling_corporate,
                                       args=(utility, start_time, lunch_time, restart_time, busy_time, end_time))
        thread_corp.start()

    # Execute playing Game.
    if opt_exec_game:
        play_game(utility, start_time, lunch_time, restart_time, busy_time, end_time, is_repo=opt_exec_repo)

    utility.print_message(NOTE, 'Finish {}'.format(file_name))
