[![channel icon](https://patrolavia.github.io/telegram-badge/follow.png)](https://t.me/farecito_eu)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/brivadeneira/)


# farecito 🚌
farecito (*/faɾeˈθito/*) helps travelers to find cheap [FlixBus](https://www.flixbus.com/) trips.
> The project name is a combination of the English word "fare" and the Spanish diminutive "cito."

It is built with free software and open source technologies 🧡.

## Introduction
Farecito is a project that allows users to find cheap [FlixBus](https://www.flixbus.com/) trips between popular cities.
It gets all cities and connections from [flixbus.com](https://www.flixbus.com/bus-routes),
including **USA**, **Brasil** and **Europe**.

![](https://i.ytimg.com/vi/fpGQoFZLb-4/maxresdefault.jpg)
*["Mochilero" reference]((https://www.youtube.com/watch?v=qYc8D0fVveM))*

## Features
- Scrapes data from [flixbus.com](https://www.flixbus.com) for all [bus routes](https://www.flixbus.com/bus-routes).
- Builds a corresponding graph in a [neo4j](https://neo4j.com/) database instance.
- Periodically captures snapshots of prices with high discounts (50% off) for popular cities.
- Sends cheap ticket alerts through a [Telegram channel](https://t.me/farecito_eu).

### TODO
- Add `BRA` and `USA` channels
- Create topics/filters for receiving just cities of interest.

## General structure

![](https://i.imgur.com/LkORYOt.png)
*Dotted lines indicate non implemented modules*

## Installation and usage

* **python version**: 3.11

```shell
~$ git clone https://github.com/brivadeneira/farecito.git
~$ conda create -n farecito python=3.11
~$ pip install -r requirements.txt
```

### .env variables

```shell
~$ mv .env.example .env
~$ nano .env
```

fill the env values:
- Aura Instance's credentials: it must be downloaded when creating the instance.
  - `NEO4J_URI`
  - `NEO4J_USERNAME`
  - `NEO4J_PASSWORD`
  - `AURA_INSTANCEID`
  - `AURA_INSTANCENAME`
- `TELEGRAM_BOT_TOKEN`: Got when creating a telegram bot, according to: https://core.telegram.org/bots/tutorial
- `TELEGRAM_CHAT_ID`: The alert channel chat, *(the bot must be admin)*.


```shell
~$ python main.py
```

## Testing

```shell
~$ pip install -r dev-requirements.txt
~$ pytest -v
~$ # run a specific test
~$ pytest tests/<path to test_file>/test_<name of file>.py::<NameOfTestClass>::test_<name_of_test>
```

## Doc
Please, visit the [wiki](https://github.com/brivadeneira/farecito/wiki) for more details.

## License
Farecito is licensed under the MIT License.
