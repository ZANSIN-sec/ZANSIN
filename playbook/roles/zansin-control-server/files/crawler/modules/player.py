#!/bin/env python
# -*- coding: utf-8 -*-
import os
import math
import time

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
class Player:
    def __init__(self, utility, session, session_id):
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.utility = utility

        # Player information.
        self.session = session
        self.session_id = session_id
        self.id = -1
        self.user_name = ''
        self.password = ''
        self.nick_name = ''
        self.created_at = ''
        self.level = 0
        self.exp = 0
        self.gold = 0
        self.max_hp = 0
        self.max_stamina = 0
        self.max_str = 0
        self.need_exp = 0
        self.stamina = 0
        self.staminaupdated_at = ''
        self.weapon_id = 0
        self.armor_id = 0
        self.image = ''
        self.charge_sum = 0
        self.injustice_num = 0
        self.charge_amount_in_this_epoch = 0

    # Get Game Top.
    def get_game_top_page(self):
        self.utility.http_req_header['Content-Type'] = self.utility.api_game_top_ctype
        status, response = self.utility.send_request(self.session,
                                                     self.utility.api_game_top_method,
                                                     self.utility.api_game_top_url,
                                                     self.utility.http_req_header,
                                                     {})

        if status is False or self.utility.judge_hacked(response, self.utility.regex_hacked) is False:
            self.utility.print_message(FAIL, 'Can not access to the Game Top.')
            return False
        else:
            return True

    # Get user's information.
    def get_user_information(self, save=False):
        self.utility.http_req_header['Content-Type'] = self.utility.api_player_ctype
        status, response = self.utility.send_request(self.session,
                                                     self.utility.api_player_method,
                                                     self.utility.api_player_url,
                                                     self.utility.http_req_header,
                                                     {})

        if status is False:
            self.utility.print_message(FAIL, 'Could not connect "Player" API.')
            self.utility.write_log(40, 'id={} Could not connect "Player" API.'.format(self.utility.player_id))
            time.sleep(self.utility.loop_wait_time)
            return False
        elif response['result'] == 'ng':
            self.utility.print_message(WARNING, '{}'.format(response['msg']))
            self.utility.write_log(30, 'id={} {}'.format(self.utility.player_id, response['msg']))
            time.sleep(self.utility.loop_wait_time)
            return False
        else:
            self.utility.print_message(OK, 'Complete getting player information: {}'.format(response))
            self.utility.write_log(20, 'id={} Complete getting player information: {}'.format(self.utility.player_id, response))

            # Update user information.
            if save:
                self.id = response['id']
                self.user_name = response['user_name']
                self.password = response['password']
                self.nick_name = response['nick_name']
                self.created_at = response['created_at']
                self.level = response['level']
                self.exp = response['exp']
                self.gold = response['gold']
                self.max_hp = response['max_hp']
                self.max_stamina = response['max_stamina']
                self.max_str = response['max_str']
                self.need_exp = response['need_exp']
                self.stamina = response['stamina']
                self.staminaupdated_at = response['staminaupdated_at']
                self.weapon_id = response['weapon_id']
                self.armor_id = response['armor_id']
                self.image = response['image']

        return response

    # Delete player.
    def delete_user(self, session):
        self.utility.http_req_header['Content-Type'] = self.utility.api_delete_ctype
        status, response = self.utility.send_request(session,
                                                     self.utility.api_delete_method,
                                                     self.utility.api_delete_url,
                                                     self.utility.http_req_header,
                                                     {})

        if status is False:
            self.utility.print_message(FAIL, 'Could not connect "Delete" API.')
            self.utility.write_log(40, 'id={} Could not connect "Delete" API.'.format(self.utility.player_id))
            time.sleep(self.utility.loop_wait_time)
        elif response['result'] == 'ng':
            self.utility.print_message(WARNING, '{}'.format(response['msg']))
            self.utility.write_log(30, 'id={} {}'.format(self.utility.player_id, response['msg']))
            time.sleep(self.utility.loop_wait_time)
        else:
            # Delete player.
            self.utility.print_message(OK, 'Complete delete player.')
            self.utility.write_log(20, 'id={} Complete delete player.'.format(self.utility.player_id))

        return

    # Execute Stamina API.
    def recovery(self):
        self.utility.api_recovery_params['price'] = self.utility.recovery_gold
        self.utility.http_req_header['Content-Type'] = self.utility.api_recovery_ctype
        status, response = self.utility.send_request(self.session,
                                                     self.utility.api_recovery_method,
                                                     self.utility.api_recovery_url,
                                                     self.utility.http_req_header,
                                                     self.utility.api_recovery_params)

        if status is False:
            self.utility.print_message(FAIL, 'Could not connect "Recovery" API.')
            self.utility.write_log(40, 'id={} Could not connect "Recovery" API.'.format(self.utility.player_id))
            time.sleep(self.utility.loop_wait_time)
            return False
        elif response['result'] == 'ng':
            self.utility.print_message(WARNING, '{}'.format(response['msg']))
            self.utility.write_log(30, 'id={} {}'.format(self.utility.player_id, response['msg']))
            return False
        else:
            # Update user's status.
            if self.get_user_information(save=True) is False:
                return False

            return True

    # Recovery stamina.
    def recovery_stamina(self, necessary_stamina):
        # Stamina loop.
        loop_flag = True
        loop_count = 0
        try:
            while loop_flag and loop_count < self.utility.max_stamina_loop_num:
                # Recovery stamina.
                if self.gold >= self.utility.recovery_gold:
                    # Execute recovery.
                    api_status = self.recovery()
                    if api_status is False:
                        # Retry.
                        time.sleep(self.utility.loop_wait_time)
                    else:
                        # Update stamina.
                        # self.stamina += self.utility.recovery_gold
                        loop_flag = False
                        self.utility.print_message(OK, 'Current stamina: {}.'.format(self.stamina))
                        self.utility.write_log(20, 'id={} Current stamina: {}.'.format(self.utility.player_id, self.stamina))
                else:
                    # When not enough gold, player charges gold using real money (price).
                    self.utility.print_message(WARNING, 'You have not enough gold for recovery stamina.')
                    self.utility.print_message(WARNING, 'You charge gold using real money!!')
                    if self.charge_gold(self.utility.stamina_charge_price) is False:
                        # Retry.
                        time.sleep(self.utility.loop_wait_time)
                loop_count += 1
            return True
        except Exception as e:
            self.utility.print_message(FAIL, 'Could not recovery stamina: {}'.format(e.args))
            time.sleep(self.utility.loop_wait_time)
            return False

    # Get battle course.
    def get_battle_course(self):
        self.utility.http_req_header['Content-Type'] = self.utility.api_get_course_ctype
        status, response = self.utility.send_request(self.session,
                                                     self.utility.api_get_course_method,
                                                     self.utility.api_get_course_url,
                                                     self.utility.http_req_header,
                                                     {})

        if status is False:
            self.utility.print_message(FAIL, 'Could not connect "Getting battle course" API.')
            self.utility.write_log(40, 'id={} Could not connect "Getting battle course" API.'.format(self.utility.player_id))
            time.sleep(self.utility.loop_wait_time)
            return None
        elif response['result'] == 'ng':
            self.utility.print_message(WARNING, '{}'.format(response['msg']))
            self.utility.write_log(30, 'id={} {}'.format(self.utility.player_id, response['msg']))
            time.sleep(self.utility.loop_wait_time)
            return None
        else:
            self.utility.print_message(OK, 'Complete getting battle courses: {}'.format(response['course']))
            self.utility.write_log(20, 'id={} Complete getting battle courses: {}'.format(self.utility.player_id, response['course']))
            return response['course']

    # select battle course.
    def select_battle_course(self, course_id):
        self.utility.api_post_course_params['id'] = course_id
        self.utility.http_req_header['Content-Type'] = self.utility.api_post_course_ctype
        status, response = self.utility.send_request(self.session,
                                                     self.utility.api_post_course_method,
                                                     self.utility.api_post_course_url,
                                                     self.utility.http_req_header,
                                                     self.utility.api_post_course_params)

        if status is False:
            self.utility.print_message(FAIL, 'Could not connect "Selecting battle course" API.')
            self.utility.write_log(40, 'id={} Could not connect "Selecting battle course" API.'.format(self.utility.player_id))
            time.sleep(self.utility.loop_wait_time)
            return False
        elif response['result'] == 'ng':
            self.utility.print_message(WARNING, '{}'.format(response['msg']))
            self.utility.write_log(30, 'id={} {}'.format(self.utility.player_id, response['msg']))

            # Lacking stamina.
            if 'lacking' in response['msg'].lower():
                msg = 'course_id={}, max_stamina={}, current_stamina={}.'.format(course_id, self.max_stamina, self.stamina)
                self.utility.print_message(WARNING, msg)
                return None
            else:
                return False
        else:
            self.utility.print_message(OK, 'Complete selecting battle course: {}.'.format(response))
            self.utility.write_log(20, 'id={} Complete selecting battle course: {}.'.format(self.utility.player_id, response))
            return response

    # Execute battle.
    def execute_battle(self, course_info):
        self.utility.http_req_header['Content-Type'] = self.utility.api_battle_ctype
        status, response = self.utility.send_request(self.session,
                                                     self.utility.api_battle_method,
                                                     self.utility.api_battle_url,
                                                     self.utility.http_req_header,
                                                     course_info)

        if status is False:
            self.utility.print_message(FAIL, 'Could not connect "Battle" API.')
            self.utility.write_log(40, 'id={} Could not connect "Battle" API.'.format(self.utility.player_id))
            time.sleep(self.utility.loop_wait_time)
            return False
        elif response['result'] == 'ng':
            self.utility.print_message(WARNING, '{}'.format(response['msg']))
            self.utility.write_log(30, 'id={} {}'.format(self.utility.player_id, response['msg']))
            time.sleep(self.utility.loop_wait_time)
            return False
        else:
            self.utility.print_message(OK, 'Complete battle.')
            self.utility.write_log(20, 'id={} Complete battle.'.format(self.utility.player_id))
            return response

    # Charge gold using real money (price).
    def charge_gold(self, charge_price):
        self.utility.api_charge_params['price'] = charge_price
        self.utility.http_req_header['Content-Type'] = self.utility.api_charge_ctype
        status, response = self.utility.send_request(self.session,
                                                     self.utility.api_charge_method,
                                                     self.utility.api_charge_url,
                                                     self.utility.http_req_header,
                                                     self.utility.api_charge_params)

        if status is False:
            self.utility.print_message(FAIL, 'Could not connect "Recovery" API.')
            self.utility.write_log(40, 'id={} Could not connect "Recovery" API.'.format(self.utility.player_id))
            time.sleep(self.utility.loop_wait_time)
            return False
        elif response['result'] == 'ng':
            self.utility.print_message(WARNING, '{}'.format(response['msg']))
            self.utility.write_log(30, 'id={} {}'.format(self.utility.player_id, response['msg']))
            time.sleep(self.utility.loop_wait_time)
            return False
        else:
            # Stack charge amount in this epoch.
            self.utility.print_message(NOTE, 'Stack charge amount in this epoch: {}.'.format(charge_price))
            self.charge_amount_in_this_epoch += charge_price

            # Update player's gold.
            self.utility.write_log(20, 'id={} Charge gold {} [{}].'.format(self.utility.player_id,
                                                                           charge_price,
                                                                           self.file_name))

            # Update charge amount.
            if self.get_user_information(save=True) is False:
                return False
            self.charge_sum += charge_price
            # self.gold += charge_price
            self.utility.print_message(OK, 'Complete charge gold: {}.'.format(charge_price))
            self.utility.write_log(20, 'id={} Complete charge gold: {}.'.format(self.utility.player_id, charge_price))
            return True

    # Execute Gatya.
    def execute_gatya(self, gatya_gold):
        self.utility.api_gatya_params['gold'] = gatya_gold
        self.utility.http_req_header['Content-Type'] = self.utility.api_gatya_ctype
        status, response = self.utility.send_request(self.session,
                                                     self.utility.api_gatya_method,
                                                     self.utility.api_gatya_url,
                                                     self.utility.http_req_header,
                                                     self.utility.api_gatya_params)

        if status is False:
            self.utility.print_message(FAIL, 'Could not connect "Gatya" API.')
            self.utility.write_log(40, 'id={} Could not connect "Gatya" API.'.format(self.utility.player_id))
            time.sleep(self.utility.loop_wait_time)
            return False
        elif response['result'] == 'ng':
            self.utility.print_message(WARNING, '{}'.format(response['msg']))
            self.utility.write_log(30, 'id={} {}'.format(self.utility.player_id, response['msg']))
            time.sleep(self.utility.loop_wait_time)
            return False
        else:
            self.utility.print_message(OK, 'Complete gatya: {}.'.format(response))
            self.utility.write_log(20, 'id={} Complete gatya: {}.'.format(self.utility.player_id, response))
            return response

    # Play game.
    def play_game(self):
        try:
            # Get top page response (connection / falsification check).
            if self.get_game_top_page() is False:
                return False

            # Initialize charge amount in this epoch.
            self.charge_amount_in_this_epoch = 0

            # Get user's information from API.
            user_status_from_api = self.get_user_information()
            if user_status_from_api is False:
                return False

            # Check Falsification.
            judge_result = self.utility.judge_falsification(self)
            if judge_result is False:
                self.injustice_num += 1
                self.utility.print_message(WARNING, 'Current injustice number: {}.'.format(self.injustice_num))
                self.utility.write_log(30, 'id={} Current injustice number: {}.'.format(self.utility.player_id, self.injustice_num))
            elif judge_result is None:
                self.utility.print_message(WARNING, 'Could not judgement.')
                return False

            # Select battle course.
            course_list = self.get_battle_course()
            if course_list is None:
                self.utility.print_message(WARNING, 'Could not get battle course.')
                time.sleep(self.utility.loop_wait_time)
                return False

            # Select battle course.
            course_select_flag = True
            loop_count = 0
            course_id = None
            while course_select_flag and loop_count < self.utility.max_course_loop_num:
                course_id = self.utility.select_battle_course_id(self, course_list)
                if course_id == -1:
                    # Recovery Stamina.
                    self.utility.write_log(30, 'id={} You are not enough stamina [{}].'.format(self.utility.player_id,
                                                                                               self.file_name))
                    if self.recovery_stamina(course_list[0]['stamina']) is False:
                        time.sleep(self.utility.loop_wait_time)
                        return False
                elif course_id is False:
                    time.sleep(self.utility.loop_wait_time)
                    return False
                else:
                    course_select_flag = False
                loop_count += 1

            # Get battle course.
            course_select_flag = True
            loop_count = 0
            course_info = {}
            while course_select_flag and loop_count < self.utility.max_course_loop_num:
                course_info = self.select_battle_course(course_id)
                if course_info is False:
                    return False
                elif course_info is None:
                    # Recovery Stamina.
                    self.utility.write_log(30, 'id={} You are not enough stamina [{}].'.format(self.utility.player_id, self.file_name))
                    if self.recovery_stamina(course_list[course_id-1]['stamina']) is False:
                        time.sleep(self.utility.loop_wait_time)
                        return False
                else:
                    course_select_flag = False
                loop_count += 1

            # Battle loop.
            if course_info is None:
                return False
            expect_turn = math.ceil(course_info['enemy']['hp']/course_info['player']['str'])
            loop_flag = True
            loop_count = 0
            battle_result = {}
            while loop_flag and loop_count < self.utility.max_battle_loop_num:
                battle_result = self.execute_battle(course_info)
                if battle_result is False:
                    return False
                elif battle_result['status']['result'] != 'going_on':
                    loop_flag = False
                else:
                    # Set course info using result of battle.
                    course_info = battle_result
                self.utility.print_message(OK, 'Battle result: {}.'.format(battle_result['status']['result']))
                loop_count += 1

            # Check falsification.
            if battle_result['status']['result'].lower() == 'win' and loop_count != expect_turn:
                self.utility.print_message(WARNING, 'Too short battle\'s turn.')
                self.utility.write_log(30, 'id={} Too short battle\'s turn. [{}].'.format(self.utility.player_id, self.file_name))
                self.utility.print_message(WARNING, 'Current injustice number: {}.'.format(self.injustice_num))
                self.utility.write_log(30, 'id={} Current injustice number: {}.'.format(self.utility.player_id, self.injustice_num))
            elif battle_result['status']['result'].lower() == 'lose':
                # Adjust battle's stamina rate.
                self.utility.battle_stamina_rate += 0.5

            # Update player's status (gold, exp..).
            if self.get_user_information(save=True) is False:
                return False

            # Gatya loop.
            if self.utility.gatya_event():
                loop_flag = True
                loop_count = 0
                gatya_amount = 0
                max_gatya_gold = self.utility.select_gatya_gold(self.level)
                self.utility.init_sr_queue()
                while loop_flag and loop_count < self.utility.max_gatya_loop_num:
                    # Execute Gatya!!
                    gatya_result = self.execute_gatya(self.utility.std_gatya_gold)
                    if gatya_result is False:
                        # API's failure.
                        return False
                    elif gatya_result['resulttype'] == 1:
                        # When not enough gold, player charges gold using real money (price).
                        self.utility.print_message(WARNING, 'You have not enough gold for gatya.')
                        self.utility.print_message(WARNING, 'You charge gold using real money!!')
                        if self.charge_gold(self.utility.gatya_charge_price) is False:
                            time.sleep(self.utility.loop_wait_time)
                    else:
                        # Check falsification.
                        if gatya_result['rarity'] == 'SR':
                            self.utility.sr_queue.append(True)
                        else:
                            self.utility.sr_queue.append(False)
                        self.utility.sr_queue.popleft()
                        if all(self.utility.sr_queue):
                            self.utility.print_message(WARNING, 'Too many super rare items.')
                            self.utility.write_log(30, 'id={} Too many super rare items. [{}].'.format(self.utility.player_id, self.file_name))
                            self.utility.print_message(WARNING, 'Current injustice number: {}.'.format(self.injustice_num))
                            self.utility.write_log(30, 'id={} Current injustice number: {}.'.format(self.utility.player_id, self.injustice_num))
                            return False

                        # Count gatya's amount.
                        gatya_amount += self.utility.std_gatya_gold
                        if max_gatya_gold > gatya_amount:
                            self.utility.print_message(WARNING, 'One more gatya: {}G/{}G.'.format(gatya_amount, max_gatya_gold))
                        else:
                            loop_flag = False
                    loop_count += 1
            else:
                self.utility.print_message(WARNING, 'Gatya\'s event didn\'t occur.')

            # Update player's status (armor_id, weapon_id).
            if self.get_user_information(save=True) is False:
                return False

            # Stamina is zero after battle.
            self.stamina = 0

            return True
        except Exception as e:
            self.utility.print_message(FAIL, 'Could not play game..')
            return False
