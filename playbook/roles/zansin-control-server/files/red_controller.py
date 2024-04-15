"""
Implement a controller for the red modules (attack tool, crawler, judge) like the ZANSIN command.
"""
import os
import socket
import random
import sys
import threading
import configparser
import sqlite3
from datetime import datetime, timedelta
from docopt import docopt

from crawler.crawler_controller import crawler_execution, get_judge_crawler_result
from attack.attack_controller import atk_execution
from judge.judge_controller import judge_execution_attack, get_judge_attack_result


# Display banner.
def show_banner():
    banner = """
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
██████╗ ███████╗██████╗        ██████╗ ██████╗ ███╗   ██╗████████╗██████╗  ██████╗ ██╗     ██╗     ███████╗██████╗ 
██╔══██╗██╔════╝██╔══██╗      ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██║     ██║     ██╔════╝██╔══██╗
██████╔╝█████╗  ██║  ██║█████╗██║     ██║   ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║     ██║     █████╗  ██████╔╝
██╔══██╗██╔══╝  ██║  ██║╚════╝██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║     ██║     ██╔══╝  ██╔══██╗
██║  ██║███████╗██████╔╝      ╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╔╝███████╗███████╗███████╗██║  ██║
╚═╝  ╚═╝╚══════╝╚═════╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""" + 'by ' + os.path.basename(__file__)
    print(banner)


# Define command option.
__doc__ = """{f}
usage:
    {f} -n <name> -t <training-server-ip> -c <control-server-ip> -a <attack-scenario>
    {f} -h | --help
options:
    -n <name>                 : Leaner name (e.g., Taro Zansin).
    -t <training-server-ip>   : ZANSIN Training Machine's IP Address (e.g., 192.168.0.5).
    -c <control-server-ip>    : ZANSIN Control Server's IP Address (e.g., 192.168.0.6).
    -a <attack-scenario>      : Attack Scenario Number (e.g., 1).
    -h --help Show this help message and exit.
""".format(f=__file__)


# Finding free high port for attack.
def find_free_high_port(control_server_ip, max_num_finding_high_port):
    for _ in range(max_num_finding_high_port):
        port = random.randint(1025, 65535)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            res = s.connect_ex((control_server_ip, port))
            if res != 0:
                return port
    return None


# Calling the Crawler.
def execute_crawler(learner_name, target_host, start_time, end_time, user_agent):
    crawler_execution(learner_name, target_host, start_time, end_time, user_agent)


# Calling the Attack tool.
def execute_attack_tool(target_host_ip, self_host_ip, self_host_port, attack_scenario_num, user_agent):
    atk_execution(target_host_ip, self_host_ip, self_host_port, attack_scenario_num, user_agent)


# Judge technical point against attack.
def judge_attack(target_host_ip):
    # Evaluate technical point.
    judge_execution_attack(target_host_ip)
    return get_judge_attack_result()


# Judge crawler point (operation ratio) against crawler.
def judge_crawler(learner_name):
    return get_judge_crawler_result(learner_name)


# Display score.
def display_score(technical_point, operation_ratio):
    print_score = '''
    +----------------------------------+----------------------------------+
    | Technical Point (Max 100 point)  | Operation Ratio (Max 100 %)      |
    |----------------------------------+----------------------------------+
    | Your Score : {} point            | Your Operation Ratio : {} %      |
    +----------------------------------+----------------------------------+
    '''
    print(print_score.format(technical_point, operation_ratio))


# Calling the Judge and Display score.
def execute_judge(target_host_ip, leaner_name):
    display_score(judge_attack(target_host_ip), judge_crawler(leaner_name))


def get_training_time(training_hours: int = 4) -> str:
    if not isinstance(training_hours, int):
        raise Exception('The format of the training time is incorrect.')

    training_start_date = datetime.now()
    training_end_date = training_start_date + timedelta(hours=training_hours)
    return training_start_date, training_end_date


# Main.
if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    full_path = os.path.dirname(os.path.abspath(__file__))

    try:
        # Get command argument.
        args = docopt(__doc__)
        arg_leaner = args['-n']
        arg_training_server_ip = args['-t']
        arg_control_server_ip = args['-c']
        arg_attack_scenario = int(args['-a'])

        # Read config.ini.
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'config.ini'), encoding='utf-8')

        # Show banner.
        show_banner()

        # Find free high port for attack.
        control_server_port = find_free_high_port(arg_control_server_ip,
                                                  int(config['Common']['max_num_finding_high_port']))
        if control_server_port is None:
            raise Exception('There are no available TCP ports on this server.')

        # Get training time.
        start_time, end_time = get_training_time(int(config['Common']['training_hours']))

        # Define modules and arguments for threading.
        thread_crawler = threading.Thread(target=execute_crawler, args=(arg_leaner,
                                                                        arg_training_server_ip,
                                                                        start_time,
                                                                        end_time,
                                                                        config['Common']['user-agent']))
        thread_attack_tool = threading.Thread(target=execute_attack_tool, args=(arg_training_server_ip,
                                                                                arg_control_server_ip,
                                                                                control_server_port,
                                                                                arg_attack_scenario,
                                                                                config['Common']['user-agent']))

        # Execute threads.
        thread_crawler.start()
        thread_attack_tool.start()

        # Join each thread.
        thread_crawler.join()
        thread_attack_tool.join()

        # Execute Judge.
        execute_judge(arg_training_server_ip, arg_leaner)
    except Exception as e:
        print(e.args)
        sys.exit()
