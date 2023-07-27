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


## Installation and usage

```shell
~$ git clone https://github.com/brivadeneira/farecito.git
~$ conda create -n farecito python=3.10
~$ pip install -r requirements.txt
```

### .env variables

```shell
~$ mv .env.example .env
~$ nano .env
```

fill the env values:
- Aura Instance's credentials: it must be downloaded when creating the instance
- `TELEGRAM_BOT_TOKEN`: Got when creating a telegram bot, according to: https://core.telegram.org/bots/tutorial

## Installation and usage

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
