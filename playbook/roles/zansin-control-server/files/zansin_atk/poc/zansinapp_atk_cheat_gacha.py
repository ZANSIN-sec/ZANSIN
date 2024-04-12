#!/usr/bin/env python
# coding: UTF-8
import time
import requests
import sys
import hashlib
import random
import string
import json
from os import urandom

#proxy
#proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
proxies = {"http": None,"https": None}

#connect timeout, read timeout
timeoutvalue= (5.0, 5.5)


def randomstr(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def new_user(target):
    session = requests.Session()
    set_id = hashlib.sha256(urandom(10)).hexdigest()
    set_password = urandom(10).hex()
    nickname_token = hashlib.md5(urandom(10)).hexdigest()[:10]
    set_nickname = "Tetsuzo" + "_" + nickname_token

    json_data = { "user_name": set_id, "password": set_password, "nick_name": set_nickname}      
    headers = { "Content-Type": "application/json" }
    target_url = "http://" + target + "/create"
    response1 = session.post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

    # print(f"userid: {set_id}")
    # print(f"password: {set_password}")
    # print(f"nick_name: {set_nickname}")
    # print("-----create user-----")
    # print("Status code:   %i" % response1.status_code)
    # print("Response body: %s" % response1.text)

    json_data = { "user_name": set_id, "password": set_password} 
    target_url = "http://" + target + "/login"
    response2 = session.post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)

    # print("-----login-----")
    # print("Status code:   %i" % response2.status_code)
    # print("Response body: %s" % response2.text)
    return session


def main():
    sr_count = 0

    argv = sys.argv
    if len(argv) == 1:
        print('IP address must be specified.')
        return
    target = argv[1]

    if not argv[2].replace('.', '').isdigit():
        print('argv[2] must be float.')
        return
    interval = float(argv[2])

    if not argv[3].replace('.', '').isdigit():
        print('argv[3] must be int.')
        return
    count = int(argv[3])

    #=====================================================================
    # Create user and Login
    #=====================================================================
    session = new_user(target)

    #=====================================================================
    # Start Gacha cheat
    #=====================================================================
    for i in range(count):
        try:
            time.sleep(float(interval))
        except ValueError:
            print('argv[2] must be float.')
            return

        # print('-'*8)
        # print(f'Epoch {i}')
        # print('Supoer Rare count:', sr_count)

        try:
            json_data = { "gold": 0 }      
            headers = { "Content-Type": "application/json" }
            target_url = "http://" + target + "/gacha"
            response = session.post(target_url, data=json.dumps(json_data), headers=headers, proxies=proxies, timeout=timeoutvalue)
            ret = json.loads(response.text)
            #print(ret['type'], ret['rarity'], ret['name'])

            if ret['rarity'] == 'SR' and ret['type'] == 'weapon':
                session = new_user(target)
                sr_count += 1

            if ret['rarity'] == 'SR' and ret['type'] == 'armor':
                session = new_user(target)
                sr_count += 1

        except requests.HTTPError as e:
            print(f'HTTP error: {e}')
            continue

        except Exception as e:
            print(f'Unknown error: {e}')
            continue


if __name__ == '__main__':
    main()