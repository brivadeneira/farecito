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
(WIP)
```shell
~$ git clone <path_to_this_repo>
~$ conda create -n farecito python=3.10
~$ pip install -r requirements.txt
```


## Testing
```shell
~$ pip install -r dev-requirements.txt
~$ pytest -v
~$ # run a specific test
~$ pytest tests/<path to test_file>/test_<name of file>.py::<NameOfTestClass>::test_<name_of_test>
```

## License
Farecito is licensed under the MIT License.
