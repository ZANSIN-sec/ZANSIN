"""
Implement a controller for the red modules (attack tool, crawler, judge) like the ZANSIN command.
"""
import os
import threading
import configparser
from datetime import datetime, timedelta
from docopt import docopt

from crawler.crawler_controller import crawler_execution
from zansin_atk.atk_controller import atk_execution
from zansinjudgepy.judge_controller import judge_execution


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
    {f} -n <name> -t <training-server-ip> -c <control-server-ip> -p <control-server-port> -a <attack-scenario>
    {f} -h | --help
options:
    -n <name>                 : Leaner name (e.g., Taro Zansin).
    -t <training-server-ip>   : Training Server IP Address (e.g., 192.168.0.5).
    -c <control-server-ip>    : Control Server IP Address (e.g., 192.168.0.6).
    -p <control-server-port>  : Control Server Port Number (e.g., 8080).
    -a <attack-scenario>      : Attack Scenario Number (e.g., 1).
    -h --help Show this help message and exit.
""".format(f=__file__)


# Calling the Crawler.
def execute_crawler(learner_name, target_host, start_time, end_time, user_agent):
    print('crawler.')
    #crawler_execution(learner_name, target_host, start_time, end_time, user_agent)


# Calling the Attack tool.
def execute_attack_tool(target_host_ip, self_host_ip, self_host_port, attack_scenario_num, user_agent):
    print('attack tool')
    atk_execution(target_host_ip, self_host_ip, self_host_port, attack_scenario_num, user_agent)


# Calling the Judge.r
def execute_judge(target_host_ip):
    print('Judge!!')
    judge_execution(target_host_ip)


# Delete table records of crawler.
def delete_table_crawler():
    print('Delete crawler table!!')


# Delete table records of attack tool.
def delete_table_attack_tool():
    print('Delete attack tool table!!')


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
        arg_control_server_port = args['-p']
        arg_attack_scenario = int(args['-a'])

        # Read atk_config.ini.
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'config.ini'), encoding='utf-8')

        # Show banner.
        show_banner()

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
                                                                                arg_control_server_port,
                                                                                arg_attack_scenario,
                                                                                config['Common']['user-agent']))

        # Execute threads.
        thread_crawler.start()
        thread_attack_tool.start()

        # Join each thread.
        thread_crawler.join()
        thread_attack_tool.join()

        # Execute Judge.
        execute_judge(arg_training_server_ip)

        # Delete records of crawler and attack tool.
        delete_table_crawler()
        delete_table_attack_tool()
    except Exception as e:
        print(e.args)

