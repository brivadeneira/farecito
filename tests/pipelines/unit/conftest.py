"""
Pipeline unit tests fixtures
"""

import pytest


@pytest.fixture
def test_cheap_trip():
    return {
        "from_city_name": "Berlin",
        "to_city_name": "Paris",
        "departure_city_uuid": "40d8f682-8646-11e6-9066-549f350fcb0c",
        "arrival_city_uuid": "40de8964-8646-11e6-9066-549f350fcb0c",
        "departure_date": "2024-07-26T00:00:00+02:00",
        "uid": "ic:d73477d0-4b42-44f5-9593-037c4b0b6e11"
        "-d78eb493a279:dcc15c7e-9603-11e6-9066-549f350fcb0c"
        "-4df8-b13e-49032fc5d07c",
        "status": "available",
        "provider": "flixbus",
        "duration_hours": 19,
        "duration_minutes": 25,
        "price_total": 2.98,
        "seats_available": 20,
    }
