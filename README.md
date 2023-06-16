# farecito 🚌
farecito (*/faɾeˈθito/*) helps travelers to find cheap [FlixBus](https://www.flixbus.com/) trips.
> The project name is a combination of the English word "fare" and the Spanish diminutive "cito."

It is built with free software and open source technologies 🧡.

## Introduction
Farecito is a project that allows users to find cheap [FlixBus](https://www.flixbus.com/) trips between popular cities.
It gets all cities and connections from [flixbus.com](https://www.flixbus.com/bus-routes),
including **USA**, **Brasil** and **Europe**, and builds the corresponding graph in a [neo4j](https://neo4j.com/)
database instance, in order to use it to search for cheap trips in an efficient way.

![](https://i.ytimg.com/vi/fpGQoFZLb-4/maxresdefault.jpg)
*["Mochilero" reference]((https://www.youtube.com/watch?v=qYc8D0fVveM))*

## TODO

- [ ] Asynchronous script that gets all cities and connections from [flixbus.com](https://www.flixbus.com/bus-routes)
and builds the corresponding graph in a [neo4j](https://neo4j.com/) database instance.
- [ ] Search for **1.99€** offers between popular cities.
- [ ] Publish the offers mentioned above in twitter.
- [ ] Build a telegram bot for processing custom cheap trip searches.

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

## Troubleshooting
- `E   TypeError: unsupported operand type(s) for |: 'type' and 'type'`
  - **description**: incompatibility between the new use of pipe (`|`) instead of `or` and pydantic types validation
  - **how to solve**: `pydantic==1.10.9` and `python 3.10` (or higher?)
- `<NameOfAClass>TestCase has no attribute <name_of_fixture>` *(in conftest.py)*
  - **description**:  unittest.TestCase methods cannot directly receive fixture function arguments
  - **how to solve**: *"inject"* fixtures with a class method as follows:
```python
@pytest.fixture(autouse=True)
def __inject_fixtures(self, mocker):
    self.mocker = mocker
```

## License
Farecito is licensed under the MIT License.
