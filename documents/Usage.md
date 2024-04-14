# Usage

## Before starting the exercise

To enable repeated exercise, let's take a snapshot of the current machines if you can.

## Start the exercise

### ZANSIN Control Server

- Log in to the Control Server via SSH using the credential `zansin`/`Passw0rd!23`.

### ZANSIN Training Machine

- Log in to the Trainign Machine via SSH using the credential `vendor`/`Passw0rd!23`.
- Before cyber attacks or cheating behaviors within the game become widespread, let's assess the environment and address any areas where corrections can be made.
- For detailed information about the environment on the ZANSIN Training Machine, please refer to the [Scenario - MINIQ UEST](./MINIQUEST.md) page.

### Start the exercise

Once you have prepared the ZANSIN Control Server and the ZANSIN Training Machine, execute the `Red Controller` to start the exercise! Note that the **Red Controller** is responsible for crawling and attacking the ZANSIN Training Machine.

#### Activate Virtual Environment

Red Controller is executed using "red_controller_venv", a Python virtual environment for ZANSIN. So, activate the Red controller virtual environment by executing the following command.

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

You execute Red Controller with the following command options.

```bash
(red_controller_venv) zansin@hostname:~$ cd red-controller/
(red_controller_venv) zansin@hostname:~/red-controller$ python3 red_controller.py -h
usage:
    red_controller.py -n <name> -t <training-server-ip> -c <control-server-ip> -p <control-server-port> -a <attack-scenario>
    red_controller.py -h | --help
options:
    -n <name>                 : Leaner name (e.g., Taro Zansin).
    -t <training-server-ip>   : ZANSIN Training Machine's IP Address (e.g., 192.168.0.5).
    -c <control-server-ip>    : ZANSIN Control Server's IP Address (e.g., 192.168.0.6).
    -p <control-server-port>  : ZANSIN Control Server's Port Number (e.g., 8080).
    -a <attack-scenario>      : Attack Scenario Number (e.g., 1).
    -h --help Show this help message and exit.
```

An example of executing **Red Controller** is shown below.

```bash
(red_controller_venv) zansin@hostname:~/red-controller$ python3 red_controller.py -n first_learner -t 192.168.0.5 -c 192.168.0.6 -p 8080 -a 1
```
By the way, the option `-a` (attack scenario) specifies the attack scenario number to be used for exercise.  
The current version of ZANSIN provides the following attack scenarios, so you can choose your favorite scenario for your enjoyment!

#### Attack Scenarios

TBD

## Check your score

When the exercise is finished, the following scores are displayed on the screen.

```bash
+----------------------------------+----------------------------------+
| Technical Point (Max 100 point)  | Operation Ratio (Max 100 %)      |
|----------------------------------+----------------------------------+
| Your Score : 70 point            | Your Operation Ratio : 60 %      |
+----------------------------------+----------------------------------+
```

The `Technical Point` on the left side is technical point that evaluate whether the attack was properly handled. The `Operation Ratio` on the right side is the percentage of the game that the crawler was able to execute correctly (operation ratio) throughout the entire exercise.

Good luck with getting a perfect score on both!
