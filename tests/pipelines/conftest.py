"""
This module contains fixtures for testing Scrapers.
"""

import pytest


@pytest.fixture
def flixbus_busstations_parsed_data_mock():
    # data_mock = MagicMock()
    # TODO improve fake data generation
    data = [
        {
            "id": 2015,
            "name": "Paris",
            "uuid": "40de8964-8646-11e6-9066-549f350fcb0c",
            "location": {"lon": 2.380503, "lat": 48.835334},
            "search_volume": 6498100,
            "reachable": [
                {"id": 1965, "uuid": "40de8463-8646-11e6-9066-549f350fcb0c", "slug": "metz"},
                {"id": 4468, "uuid": "40e01d5a-8646-11e6-9066-549f350fcb0c", "slug": "limoges"},
                {"id": 4018, "uuid": "40dff20a-8646-11e6-9066-549f350fcb0c", "slug": "avignon"},
            ],
            "region": "EU",
        },
        {
            "id": 88,
            "name": "Berlin",
            "uuid": "40d8f682-8646-11e6-9066-549f350fcb0c",
            "location": {"lon": 13.404616, "lat": 52.486081},
            "search_volume": 5894700,
            "reachable": [
                {"id": 113, "uuid": "40d917f9-8646-11e6-9066-549f350fcb0c", "slug": "leipzig"},
                {"id": 1394, "uuid": "40de1f31-8646-11e6-9066-549f350fcb0c", "slug": "wien"},
                {"id": 7588, "uuid": "40e19dd6-8646-11e6-9066-549f350fcb0c", "slug": "lodz"},
            ],
            "region": "EU",
        },
    ]

    return data


@pytest.fixture
def flixbus_busstations_processed_data_mock():
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
