# Usage

## Before starting the exercise

To enable repeated exercise, let's take a snapshot of the current machines if you can.

## Start the exercise

Once you have prepared the ZANSIN Control Server and the ZANSIN Training Machine, you need to login both **ZANSIN Contoll Server** and **ZANSIN Training Machine** via SSH.

> [!NOTE]
> **ZANSIN Controll Srver** is responsible for crawling (game play) and attacking ZANSIN training machines from the ZANSIN Control Server.
> 
> **ZANSIN Training Machine** is for what you try to fix vulnerabilities and to response incidents.

### ZANSIN Controll Server

Login to the **ZANSIN Control Server** using user `zansin` and password you set before, then execute **Red Controller** to start the exercise.

#### Activate Virtual Environment

The **Red Controller** is executed using `red_controller_venv`, a Python virtual environment. So, activate the **Red controller** virtual environment by executing the following command.

```bash
zansin@hostname:~$ source red-controller/red_controller_venv/bin/activate
(red_controller_venv) zansin@hostname:~$ 
```

> [!NOTE]
> Once you have finished the exercise, deactivate the virtual environment by executing the following command.
>```bash
>(red_controller_venv) zansin@hostname:~$ deactivate
>```

#### Execute Red Controller

You can execute **Red Controller** with the following command options.

```bash
(red_controller_venv) zansin@hostname:~$ cd red-controller/
(red_controller_venv) zansin@hostname:~/red-controller$ python3 red_controller.py -h
usage:
    red_controller.py -n <name> -t <training-server-ip> -c <control-server-ip> -a <attack-scenario>
    red_controller.py -h | --help
options:
    -n <name>                 : Leaner name (e.g., Taro Zansin).
    -t <training-server-ip>   : ZANSIN Training Machine's IP Address (e.g., 192.168.0.5).
    -c <control-server-ip>    : ZANSIN Control Server's IP Address (e.g., 192.168.0.6).
    -a <attack-scenario>      : Attack Scenario Number (e.g., 1).
    -h --help Show this help message and exit.
```

An example of executing **Red Controller** is shown below.

```bash
(red_controller_venv) zansin@hostname:~/red-controller$ python3 red_controller.py -n first_learner -t 192.168.0.5 -c 192.168.0.6 -a 1
```

By the way, the option `-a` (attack scenario) specifies the attack scenario number to be used for exercise.  
The current version of ZANSIN provides the following attack scenarios, so you can choose your favorite scenario for your enjoyment!

#### Attack Scenarios

| No. | Description |
| ---- | ---- |
| 0 | For development. Not normally used. | 
| 1 | Attempts all attack patterns depending on the situation. This is the most difficult mode. | 
| 2 | Attempts about half of the attacks. The interval between each attack is also longer than the scenario 1. |

#### Check your score

When the exercise is finished, the following scores are displayed on the screen.

```bash
+----------------------------------+----------------------------------+
| Technical Point (Max 100 point)  | Operation Ratio (Max 100 %)      |
|----------------------------------+----------------------------------+
| Your Score : 70 point            | Your Operation Ratio : 60 %      |
+----------------------------------+----------------------------------+
```

The `Technical Point` on the left side is technical point that evaluate whether the attack was properly handled. The `Operation Ratio` on the right side is the percentage of the game that the crawler was able to execute correctly (operation ratio) throughout the entire exercise.


### ZANSIN Training Machine

Login to the **ZANSIN Trainign Machine** via SSH using the credential `vendor`/`Passw0rd!23` for the exercise. <- not the `zansin` account!!

Before cyber attacks or cheating behaviors within the game become widespread, let's assess the environment and fix any vulnerabilities, not only Game APIs but also the whole environment of the ZANSIN Training Machine.

If you notice something storange behavior considere as cyber attacks or game cheating, you should try to resuponse them as soon as possible.

For more details about the environment on the ZANSIN Training Machine, please refer to the [Scenario - MINIQ UEST](./MINIQUEST.md) page.



Good luck with getting a perfect score both the **Technical Point** and **Operation Rasio**!