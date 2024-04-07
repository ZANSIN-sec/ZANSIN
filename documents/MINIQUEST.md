# Prologue

Once upon a time, there was an entrepreneur who dreamed of making a fortune. Having experienced several business failures in the past, he decided to launch an online gaming company as his new venture.

Being an authoritarian president, he himself came up with game concepts and designs, hired development partners at a very low cost, and managed to launch the service.

In such circumstances, you were hired by this company as personnel to operate the system continuously.

![Prologue](../images/fadcd3507c63f192d2a650a20be97fe6f6c286f7.png)

# MINI QUEST

The name of the launched online game is "MINI QUEST."

Inspired by Japan's immensely popular role-playing game that debuted in 1986, modern mechanisms such as a gacha system for acquiring rare items and a monetization system for purchasing in-game currency have been incorporated.

![MINI QUEST](../images/MINIQUEST.png)

# Mission


When initiating this scenario, cyber attacks and game cheating behaviors will be directed towards the online game servers that you must manage.

In an online game where cyber attacks and cheating behaviors are prevalent, such as data tampering on the online game server, service interruptions, and frequent cheating incidents, legitimate users decrease, resulting in an inability to generate profits.

You must rigorously implement the following to consistently generate revenue:

- Protect the server from cyber attacks.
- Safeguard the game from cheating behaviors.

# Scenario Environment

The structure of the online game server is as follows:
Various APIs are implemented using Docker within a single Ubuntu Linux instance.

![Environment](../images/ffab4829c784d1661a4e16e3a519b740a2769823.png)

# Game APIs

The APIs implemented in the online game are as follows:

- User Registration API
- Login API
- Withdrawal API
- Player Data API
- Upload an Image API
- Battle Course List API
- Determination of the Battle Course API
- Battle API
- Stamina Recovery API
- Gatcha API
- In-game purshase API
- Ranking API

The API reference is available for download from the following link.

- [API Refarence](../documents/API_Reference.pdf)

# Accesing MINI QUEST


When accessing the online game itself, you simply need to access the IP address of the online game server using HTTP (port 80/tcp).

`http://{IP ADDRESS}`

> [!NOTE]
> If HTTP is blocked by a firewall, port forwarding may be required to access the game through a browser.

## State Transition Diagram of MINI QUEST

The progression of the game screen is as follows:

![State Transition Diagram](../images/7863d519ae098f9a4b0601e9abcf530d880a18db.png)

## User Management

As the administrator of the online game server, you have the ability to manage game players.

`http://{IP ADDR}/user_list/`


If there is a player engaging in unauthorized cheating behavior, you can remove that player by using the "BAN!!" button.

![User Management](../images/8f0da7656246ced22aaf5c8e86765978826c4de9.png)

## User Ranking

This page allows you to check which players are performing well.
As this page is a public page, it should be accessible to everyone.

`http://{IP ADDRESS}/ranking/`

![Ranking](../images/df9bb0949da341dd1bcedc7716577472bc492ad6.png)

