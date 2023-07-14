"""
This module contains fixtures for testing Pipelines.
"""

import pytest


@pytest.fixture
def flixbus_busstations_proccesed_data_mock():
    # data_mock = MagicMock()
    # TODO improve fake data generation
    data = [
        {
            "city_id": 2015,
            "city_name": "Paris",
            "city_uuid": "40de8964-8646-11e6-9066-549f350fcb0c",
            "region": "EU",
            "location": {"lon": 2.380503, "lat": 48.835334},
            "is_popular": True,
            "reachable_ids": [1965, 4468, 4018],
        },
        {
            "city_id": 88,
            "city_name": "Berlin",
            "city_uuid": "40d8f682-8646-11e6-9066-549f350fcb0c",
            "region": "EU",
            "location": {"lon": 13.404616, "lat": 52.486081},
            "is_popular": True,
            "reachable_ids": [113, 1394, 7588],
        },
    ]
    return data
