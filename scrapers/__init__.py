"""
Models, utils and settings for scrapers:
- trips:
    - get data via http requests
    - parse, process, clean, validate and store data items
"""

from .flixbus import *
from .models import *
from .settings import *
from .utils import *
