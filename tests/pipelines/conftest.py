"""
This module contains fixtures for testing Scrapers.
"""

import pytest

from neo4j_graph import Location


@pytest.fixture
def flixbus_busstations_parsed_data_mock():
    # data_mock = MagicMock()
    # TODO [improvement] fake data generation
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
            "id": 2015,
            "city_name": "Paris",
            "city_uuid": "40de8964-8646-11e6-9066-549f350fcb0c",
            "region": "EU",
            "location": Location(latitude=48.835334, longitude=2.380503),
            "is_popular": True,
            "reachable_ids": [1965, 4468, 4018],
        },
        {
            "id": 88,
            "city_name": "Berlin",
            "city_uuid": "40d8f682-8646-11e6-9066-549f350fcb0c",
            "region": "EU",
            "location": Location(latitude=52.486081, longitude=13.404616),
            "is_popular": True,
            "reachable_ids": [113, 1394, 7588],
        },
    ]

    return data


@pytest.fixture
def flixbus_trips_test_response():
    # TODO refactor this!
    return {
        "response_uuid": "ac961ec8-8aca-4d3c-9841-c74d3a4cf6f7",
        "trips": [
            {
                "departure_city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                "arrival_city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                "date": "2023-07-26T00:00:00+02:00",
                "results": {
                    "ic:d73477d0-4b42-44f5-9593-037c4b0b6e11fc5d07c": {
                        "uid": "ic:d7341e6-9066-549f350fcb0c:e3e50bdc-1132-49032fc5d07c",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T00:10:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "d73477d0-4b42-44f5-9593-037c4b0b6e11",
                        },
                        "arrival": {
                            "date": "2023-07-26T19:35:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 19, "minutes": 25},
                        "price": {"total": 2.98, "original": 82.98, "average": 82.98},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "medium",
                        },
                        "available": {"seats": 20, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T00:10:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "d73477d0-4b42-44f5-9593-037c4b0b6e11",
                                },
                                "arrival": {
                                    "date": "2023-07-26T09:40:00+02:00",
                                    "city_id": "40e07fbc-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc15c7e-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixpl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-26T12:35:00+02:00",
                                    "city_id": "40e07fbc-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc15c7e-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-26T19:35:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixnl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "direct:e22ea379-97aa-4a60-a06aef:1748349f350fcb0c": {
                        "uid": "direct:e22ea379-97ac5426b-96-549f350fcb0c",
                        "status": "available",
                        "transfer_type": "Fast",
                        "transfer_type_key": "fast",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T02:30:00+02:00",
                            "city_id": "40d8f682-8646-11e49f350fcb0c",
                            "station_id": "17483554-a4ab940-b5f56740014f",
                        },
                        "arrival": {
                            "date": "2023-07-26T19:45:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 17, "minutes": 15},
                        "price": {"total": 159.99, "original": 159.99, "average": 159.99},
                        "remaining": {
                            "seats_left_at_price": 3,
                            "seats": 3,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 3, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T02:30:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "17483554-a4a8-4dad-b940-b5f56740014f",
                                },
                                "arrival": {
                                    "date": "2023-07-26T19:45:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixpl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            }
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                        "intermediate_stations_count": 11,
                    },
                    "direct:e22ea379-97aa-4a60-a06a-235e0a1c603-11e6-9066-549f350fcb0c": {
                        "uid": "direct:e22ea379-97aa-4a6b0c:dcc5426b-9603-11e6-9066-549f350fcb0c",
                        "status": "available",
                        "transfer_type": "Fast",
                        "transfer_type_key": "fast",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T02:55:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-26T19:45:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 16, "minutes": 50},
                        "price": {"total": 9.99, "original": 159.99, "average": 159.99},
                        "remaining": {
                            "seats_left_at_price": 3,
                            "seats": 3,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 3, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T02:55:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-26T19:45:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixpl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            }
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                        "intermediate_stations_count": 10,
                    },
                    "direct:e22ea379-97aa-4a60-a06a-235e603-11e6-9066-549f350fcb0c": {
                        "uid": "direct:e22ea379cc5426b-9603-11e6-9066-549f350fcb0c",
                        "status": "available",
                        "transfer_type": "Fast",
                        "transfer_type_key": "fast",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T03:15:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-26T19:45:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 16, "minutes": 30},
                        "price": {"total": 9.99, "original": 159.99, "average": 159.99},
                        "remaining": {
                            "seats_left_at_price": 3,
                            "seats": 3,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 3, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T03:15:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-26T19:45:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixpl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            }
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                        "intermediate_stations_count": 9,
                    },
                    "direct:a7105e21-4160-4b22-9996-15117a01eb1603-11e6-9066-549f350fcb0c": {
                        "uid": "direct:a7105e21-dcc5426b-9603-11e6-9066-549f350fcb0c",
                        "status": "available",
                        "transfer_type": "Direct",
                        "transfer_type_key": "direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T08:00:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T02:50:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 18, "minutes": 50},
                        "price": {"total": 79.99, "original": 79.99, "average": 79.99},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 16, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T08:00:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T02:50:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            }
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                        "intermediate_stations_count": 13,
                    },
                    "ic:dcbfd6bc0fcb0c:dcbada9a-abb-a591-4f20-ac6f-e5b69126d3dc": {
                        "uid": "ic:dcbfd6bc-bb-a591-4f20-ac6f-e5b69126d3dc",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T12:05:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbfd6bc-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T07:35:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 19, "minutes": 30},
                        "price": {"total": 89.98, "original": 89.98, "average": 89.98},
                        "remaining": {
                            "seats_left_at_price": 1,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 8, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T12:05:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbfd6bc-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-26T15:15:00+02:00",
                                    "city_id": "40d91e53-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbada9a-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-26T18:45:00+02:00",
                                    "city_id": "40d91e53-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbada9a-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T07:35:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "ic:dcbb994f-9603-11e6-9066-549-abd0-fa1e1ef5b32e": {
                        "uid": "ic:dcbb994f-9603-11eabd0-fa1e1ef5b32e",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T12:20:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T07:10:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 18, "minutes": 50},
                        "price": {"total": 139.98, "original": 139.98, "average": 139.98},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 14, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T12:20:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-26T16:25:00+02:00",
                                    "city_id": "40de1ad1-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbc6452-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixcz",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-26T17:15:00+02:00",
                                    "city_id": "40de1ad1-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbc6452-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T07:10:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "ic:dcbb994fbb8e-c14143bf94bf": {
                        "uid": "ic:dcbb994bf94bf",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T13:00:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T07:15:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 18, "minutes": 15},
                        "price": {"total": 104.98, "original": 104.98, "average": 104.98},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 17, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T13:00:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-26T16:50:00+02:00",
                                    "city_id": "40da4ac8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbb2109-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixpl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-26T18:20:00+02:00",
                                    "city_id": "40da4ac8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbb2109-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T07:15:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "direct:a47e0f9a-4a75-4d4e-ab6a-e6-9066-549f350fcb0c": {
                        "uid": "direct:a47e0f9a-4a75-4d4e-ab6a-c6e26b-9603-11e6-9066-549f350fcb0c",
                        "status": "available",
                        "transfer_type": "Direct",
                        "transfer_type_key": "direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T13:45:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "17483554-a4a8-4dad-b940-b5f56740014f",
                        },
                        "arrival": {
                            "date": "2023-07-27T07:45:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 18, "minutes": 0},
                        "price": {"total": 79.99, "original": 79.99, "average": 79.99},
                        "remaining": {
                            "seats_left_at_price": 3,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 21, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T13:45:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "17483554-a4a8-4dad-b940-b5f56740014f",
                                },
                                "arrival": {
                                    "date": "2023-07-27T07:45:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixpl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            }
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                        "intermediate_stations_count": 12,
                    },
                    "direct:a47e0f9a-4a75-4d11e6-9066-549f350fcb0c": {
                        "uid": "direct:a47e0f9a-4a75-4d4e-ab426b-9603-11e6-9066-549f350fcb0c",
                        "status": "available",
                        "transfer_type": "Direct",
                        "transfer_type_key": "direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T14:40:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T07:45:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 17, "minutes": 5},
                        "price": {"total": 89.99, "original": 89.99, "average": 89.99},
                        "remaining": {
                            "seats_left_at_price": 3,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 21, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T14:40:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T07:45:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixpl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            }
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                        "intermediate_stations_count": 11,
                    },
                    "ic:dcbb994fbb8e-erc14143bf94bf": {
                        "uid": "ic:dcbb994bf94bf",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "train#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T15:27:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "394a5408-d778-4959-a63e-973253443ed2",
                        },
                        "arrival": {
                            "date": "2023-07-27T07:10:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 15, "minutes": 43},
                        "price": {"total": 99.98, "original": 99.98, "average": 99.98},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "medium",
                        },
                        "available": {"seats": 39, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T15:27:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "394a5408-d778-4959-a63e-973253443ed2",
                                },
                                "arrival": {
                                    "date": "2023-07-26T20:35:00+02:00",
                                    "city_id": "40d9068f-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbac076-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "train",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "train",
                                "brand_id": "adf3cadd-7991-436c-be53-eb0f9c5ac165",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-27T00:30:00+02:00",
                                    "city_id": "40d9068f-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbac076-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T07:10:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [
                            "Please change to your FlixBus in Heidelberg. "
                            "The bus station (Alte Eppelheimer Str. 43) "
                            'is a 350m walk from the exit "Nord,Kurfürstenanlage" '
                            "of the train station."
                        ],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "ic:dcbb994fbb8esdfds-c14143bf94bf": {
                        "uid": "ic:dcbb994bf94bf",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "train#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T16:11:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "895f31c8-7f88-4d8f-a070-4b4a6320160a",
                        },
                        "arrival": {
                            "date": "2023-07-27T07:35:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 15, "minutes": 24},
                        "price": {"total": 109.98, "original": 109.98, "average": 109.98},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 22, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T16:11:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "895f31c8-7f88-4d8f-a070-4b4a6320160a",
                                },
                                "arrival": {
                                    "date": "2023-07-26T21:22:00+02:00",
                                    "city_id": "40d911c7-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaca96-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "train",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "train",
                                "brand_id": "adf3cadd-7991-436c-be53-eb0f9c5ac165",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-27T00:35:00+02:00",
                                    "city_id": "40d911c7-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaca96-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T07:35:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [
                            "Please change to your FlixBus in Düsseldorf. "
                            'The bus station "ZOB"  (Worringer Straße 140) '
                            "is a 250m walk from the main exit "
                            '"Konrad-Adenauer-Platz/Innenstadt" of the train station.'
                        ],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "ic:dcbbsfdsf994fbb8e-c14143bf94bf": {
                        "uid": "ic:dcbb994bf94bf",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "train#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T16:27:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "394a5408-d778-4959-a63e-973253443ed2",
                        },
                        "arrival": {
                            "date": "2023-07-27T07:35:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 15, "minutes": 8},
                        "price": {"total": 109.98, "original": 109.98, "average": 109.98},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 22, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T16:27:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "394a5408-d778-4959-a63e-973253443ed2",
                                },
                                "arrival": {
                                    "date": "2023-07-26T21:22:00+02:00",
                                    "city_id": "40d911c7-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaca96-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "train",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "train",
                                "brand_id": "adf3cadd-7991-436c-be53-eb0f9c5ac165",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-27T00:35:00+02:00",
                                    "city_id": "40d911c7-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaca96-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T07:35:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [
                            "Please change to your FlixBus in Düsseldorf. "
                            'The bus station "ZOB"  '
                            "(Worringer Straße 140) "
                            "is a 250m walk from the main exit "
                            '"Konrad-Adenauer-Platz/Innenstadt" of the train station.'
                        ],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "ic:dcbb9sdfsdf94fbb8e-c14143bf94bf": {
                        "uid": "ic:dcbb994bf94bf",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "train#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T16:39:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "e6f7f0f4-4bb5-45a0-bcc2-d5e7279686dd",
                        },
                        "arrival": {
                            "date": "2023-07-27T07:35:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 14, "minutes": 56},
                        "price": {"total": 109.98, "original": 109.98, "average": 109.98},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 22, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T16:39:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "e6f7f0f4-4bb5-45a0-bcc2-d5e7279686dd",
                                },
                                "arrival": {
                                    "date": "2023-07-26T21:22:00+02:00",
                                    "city_id": "40d911c7-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaca96-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "train",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "train",
                                "brand_id": "adf3cadd-7991-436c-be53-eb0f9c5ac165",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-27T00:35:00+02:00",
                                    "city_id": "40d911c7-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaca96-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T07:35:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [
                            "Please change to your FlixBus in Düsseldorf. "
                            'The bus station "ZOB"  (Worringer Straße 140) '
                            "is a 250m walk from the main exit "
                            '"Konrad-Adenauer-Platz/Innenstadt" of the train station.'
                        ],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "ic:dcbsdfdsfb994fbb8e-c14143bf94bf": {
                        "uid": "ic:dcbb994bf94bf",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T18:15:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbfd6bc-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T13:35:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 19, "minutes": 20},
                        "price": {"total": 1.98, "original": 61.98, "average": 61.98},
                        "remaining": {
                            "seats_left_at_price": 2,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 16, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T18:15:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbfd6bc-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-26T20:50:00+02:00",
                                    "city_id": "40d917f9-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbad0e0-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-26T23:35:00+02:00",
                                    "city_id": "40d917f9-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbad0e0-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T13:35:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "ic:dcbb994fbb8e-c1414sdfdsf3bf94bf": {
                        "uid": "ic:dcbb994bf94bf",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T18:25:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "17483554-a4a8-4dad-b940-b5f56740014f",
                        },
                        "arrival": {
                            "date": "2023-07-27T13:30:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 19, "minutes": 5},
                        "price": {"total": 93.98, "original": 93.98, "average": 93.98},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "medium",
                        },
                        "available": {"seats": 24, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T18:25:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "17483554-a4a8-4dad-b940-b5f56740014f",
                                },
                                "arrival": {
                                    "date": "2023-07-26T20:30:00+02:00",
                                    "city_id": "40db219f-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "a3b04e6c-8c21-464a-81c0-d823066ffdf2",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-26T23:15:00+02:00",
                                    "city_id": "40db219f-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "a3b04e6c-8c21-464a-81c0-d823066ffdf2",
                                },
                                "arrival": {
                                    "date": "2023-07-27T13:30:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixpl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "direct:7179b6b8-f736-4dea-be24-585c7603-11e6-9066-549f350fcb0c": {
                        "uid": "direct:7179b6b8-f736-4dea-be2066-549f350fcb0c",
                        "status": "available",
                        "transfer_type": "Direct",
                        "transfer_type_key": "direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T19:00:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T08:00:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 13, "minutes": 0},
                        "price": {"total": 79.99, "original": 79.99, "average": 79.99},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "medium",
                        },
                        "available": {"seats": 44, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T19:00:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T08:00:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            }
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                        "intermediate_stations_count": 1,
                    },
                    "direct:f91d4613-1b30-4ce-9066-549f350fcb0c": {
                        "uid": "direct:f91d4613-1b30-4ce2-a6b-9603-11e6-9066-549f350fcb0c",
                        "status": "available",
                        "transfer_type": "Direct",
                        "transfer_type_key": "direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T19:20:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T07:55:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 12, "minutes": 35},
                        "price": {"total": 159.99, "original": 159.99, "average": 159.99},
                        "remaining": {
                            "seats_left_at_price": 1,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 14, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T19:20:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T07:55:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            }
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                        "intermediate_stations_count": 0,
                    },
                    "ic:dcbb994sdfsdffbb8e-c14143bf94bf": {
                        "uid": "ic:dcbb994bf94bf",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T20:20:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T13:30:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 17, "minutes": 10},
                        "price": {"total": 90.98, "original": 90.98, "average": 90.98},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "medium",
                        },
                        "available": {"seats": 29, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T20:20:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-26T22:45:00+02:00",
                                    "city_id": "40db219f-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "a3b04e6c-8c21-464a-81c0-d823066ffdf2",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-26T23:15:00+02:00",
                                    "city_id": "40db219f-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "a3b04e6c-8c21-464a-81c0-d823066ffdf2",
                                },
                                "arrival": {
                                    "date": "2023-07-27T13:30:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixpl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "direct:35547998-16a1-4991-8301-36-549f350fcb0c": {
                        "uid": "direct:35547998-16a13-11e6-9066-549f350fcb0c",
                        "status": "available",
                        "transfer_type": "Direct",
                        "transfer_type_key": "direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T21:00:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T10:00:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 13, "minutes": 0},
                        "price": {"total": 89.99, "original": 89.99, "average": 89.99},
                        "remaining": {
                            "seats_left_at_price": 3,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 16, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T21:00:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T10:00:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixnl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            }
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                        "intermediate_stations_count": 3,
                    },
                    "direct:2a5a898a-291e6-9066-549f350fcb0c": {
                        "uid": "direct:2a5a898a-29b8-4354-a7a0-3a9ebb3fd350fcb0c",
                        "status": "available",
                        "transfer_type": "Direct",
                        "transfer_type_key": "direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T21:15:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T13:35:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 16, "minutes": 20},
                        "price": {"total": 79.99, "original": 9.99, "average": 79.99},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 29, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T21:15:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T13:35:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            }
                        ],
                        "messages": [],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                        "intermediate_stations_count": 13,
                    },
                    "ic:dcbb994fbb8e-cert14143bf94bf": {
                        "uid": "ic:dcbb994bf94bf",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T22:50:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "17483554-a4a8-4dad-b940-b5f56740014f",
                        },
                        "arrival": {
                            "date": "2023-07-27T16:40:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "9dc244f1-63d4-4db1-afbd-a10cc0377464",
                        },
                        "duration": {"hours": 17, "minutes": 50},
                        "price": {"total": 89.98, "original": 89.98, "average": 89.98},
                        "remaining": {
                            "seats_left_at_price": 1,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 19, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T22:50:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "17483554-a4a8-4dad-b940-b5f56740014f",
                                },
                                "arrival": {
                                    "date": "2023-07-27T08:05:00+02:00",
                                    "city_id": "40dde3b8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbdd1b1-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-27T10:00:00+02:00",
                                    "city_id": "40dde3b8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbdd1b1-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T16:40:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "9dc244f1-63d4-4db1-afbd-a10cc0377464",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixnl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [
                            "This ride is the fastest way to your destination, "
                            "please bring some water / "
                            "snacks because there won’t be any stops."
                        ],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "ic:17483554-a4a8-4dad-b940-b5-431d-9d39-33f8c7b4333a": {
                        "uid": "ic:17483554-a4141f70c6-62bd-431d-9d39-33f8c7b4333a",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T22:50:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "17483554-a4a8-4dad-b940-b5f56740014f",
                        },
                        "arrival": {
                            "date": "2023-07-27T17:25:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 18, "minutes": 35},
                        "price": {"total": 99.98, "original": 99.98, "average": 99.98},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 19, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T22:50:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "17483554-a4a8-4dad-b940-b5f56740014f",
                                },
                                "arrival": {
                                    "date": "2023-07-27T08:05:00+02:00",
                                    "city_id": "40dde3b8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbdd1b1-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-27T10:00:00+02:00",
                                    "city_id": "40dde3b8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbdd1b1-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T17:25:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixnl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [
                            "This ride is the fastest way to your destination, "
                            "please bring some water /"
                            " snacks because there won’t be any stops."
                        ],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "ic:dcbb994f-9603-11f350fcb070c6-62bd-431d-9d39-33f8c7b4333a": {
                        "uid": "ic:dcbb994f-9603-11e6-9066-549f350fcb033f8c7b4333a",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T23:15:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T16:40:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "9dc244f1-63d4-4db1-afbd-a10cc0377464",
                        },
                        "duration": {"hours": 17, "minutes": 25},
                        "price": {"total": 89.98, "original": 89.98, "average": 89.98},
                        "remaining": {
                            "seats_left_at_price": 1,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 19, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T23:15:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T08:05:00+02:00",
                                    "city_id": "40dde3b8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbdd1b1-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-27T10:00:00+02:00",
                                    "city_id": "40dde3b8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbdd1b1-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T16:40:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "9dc244f1-63d4-4db1-afbd-a10cc0377464",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixnl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [
                            "This ride is the fastest way to your destination, "
                            "please bring some water / "
                            "snacks because there won’t be any stops."
                        ],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "ic:dcbb994f-9603-11e6-90661f70c6-62bd-431d-9d39-33f8c7b4333a": {
                        "uid": "ic:dcbb994f-9603-11e6-2bd-431d-9d39-33f8c7b4333a",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T23:15:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T17:25:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        },
                        "duration": {"hours": 18, "minutes": 10},
                        "price": {"total": 99.98, "original": 99.98, "average": 99.98},
                        "remaining": {
                            "seats_left_at_price": None,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 19, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T23:15:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T08:05:00+02:00",
                                    "city_id": "40dde3b8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbdd1b1-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-27T10:00:00+02:00",
                                    "city_id": "40dde3b8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbdd1b1-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T17:25:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixnl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [
                            "This ride is the fastest way to your destination,"
                            " please bring some water / "
                            "snacks because there won’t be any stops."
                        ],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                    "ic:dcd1b1-9603-11e6-90641f70c6-62bd-431d-9d39-33f8c7b4333a": {
                        "uid": "ic:dcbaae-549f350fcb0c::141f70c6-62bd-431d-9d39-33f8c7b4333a",
                        "status": "available",
                        "transfer_type": "Transfer",
                        "transfer_type_key": "direct#direct",
                        "provider": "flixbus",
                        "departure": {
                            "date": "2023-07-26T23:40:00+02:00",
                            "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                            "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                        },
                        "arrival": {
                            "date": "2023-07-27T16:40:00+02:00",
                            "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                            "station_id": "9dc244f1-63d4-4db1-afbd-a10cc0377464",
                        },
                        "duration": {"hours": 17, "minutes": 0},
                        "price": {"total": 89.98, "original": 89.98, "average": 89.98},
                        "remaining": {
                            "seats_left_at_price": 1,
                            "seats": None,
                            "bike_slots": 0,
                            "capacity": "low",
                        },
                        "available": {"seats": 19, "bike_slots": 0},
                        "legs": [
                            {
                                "departure": {
                                    "date": "2023-07-26T23:40:00+02:00",
                                    "city_id": "40d8f682-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T08:05:00+02:00",
                                    "city_id": "40dde3b8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbdd1b1-9603-11e6-9066-549f350fcb0c",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "mfb",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                            {
                                "departure": {
                                    "date": "2023-07-27T10:00:00+02:00",
                                    "city_id": "40dde3b8-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "dcbdd1b1-9603-11e6-9066-549f350fcb0c",
                                },
                                "arrival": {
                                    "date": "2023-07-27T16:40:00+02:00",
                                    "city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
                                    "station_id": "9dc244f1-63d4-4db1-afbd-a10cc0377464",
                                },
                                "means_of_transport": "bus",
                                "amenities": ["WIFI", "POWER_SOCKETS"],
                                "is_marketplace": False,
                                "operator_id": "flixnl",
                                "brand_id": "a18f138c-68fa-4b45-a42f-adb0378e10d3",
                            },
                        ],
                        "messages": [
                            "This ride is the fastest way to your destination, "
                            "please bring some water "
                            "/ snacks because there won’t be any stops."
                        ],
                        "restrictions": {
                            "sale_restriction": False,
                            "info_title": "",
                            "info_title_hint": "",
                            "info_message": "",
                            "bikes_allowed": True,
                        },
                    },
                },
                "means_of_transport": ["bus", "train"],
                "departure": {
                    "earliest_date": "2023-07-26T00:10:00+02:00",
                    "latest_date": "2023-07-26T23:40:00+02:00",
                    "stations": [
                        "d73477d0-4b42-44f5-9593-037c4b0b6e11",
                        "17483554-a4a8-4dad-b940-b5f56740014f",
                        "dcbb994f-9603-11e6-9066-549f350fcb0c",
                        "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                        "dcbfd6bc-9603-11e6-9066-549f350fcb0c",
                        "394a5408-d778-4959-a63e-973253443ed2",
                        "895f31c8-7f88-4d8f-a070-4b4a6320160a",
                        "e6f7f0f4-4bb5-45a0-bcc2-d5e7279686dd",
                    ],
                },
                "arrival": {
                    "earliest_date": "2023-07-26T19:35:00+02:00",
                    "latest_date": "2023-07-27T17:25:00+02:00",
                    "stations": [
                        "dcc5426b-9603-11e6-9066-549f350fcb0c",
                        "9dc244f1-63d4-4db1-afbd-a10cc0377464",
                    ],
                },
            }
        ],
        "operators": {
            "flixpl": {
                "label": "FlixBus",
                "key": "flixpl",
                "url": "https://www.flixbus.pl/",
                "address": "ul. Fabryczna 5a, 00-446 Warszawa",
                "id": "flixpl",
            },
            "flixnl": {
                "label": "FlixBus",
                "key": "flixnl",
                "url": "http://flixbus.nl",
                "address": "Weesperstraat 61, 1018 VN Amsterdam",
                "id": "flixnl",
            },
            "mfb": {
                "label": "FlixBus",
                "key": "mfb",
                "url": "http://flixbus.de",
                "address": "Karl-Liebknecht-Straße 33, D-10178 Berlin",
                "id": "mfb",
            },
            "flixcz": {
                "label": "FlixBus",
                "key": "flixcz",
                "url": "https://www.flixbus.cz",
                "address": "Havlíčkova 1029/3, 110 00 Praha 1",
                "id": "flixcz",
            },
            "train": {
                "label": "FlixTrain",
                "key": "train",
                "url": "https://www.flixbus.com/",
                "address": "Friedenheimer Brücke 16, 80639  München",
                "id": "train",
            },
        },
        "brands": {
            "a18f138c-68fa-4b45-a42f-adb0378e10d3": {
                "name": "FlixBus",
                "type": "core",
                "active": True,
                "logo": "https://cdn-cf.cms.flixbus.com/drupal-assets/2023-03/flixbus-logo.png",
                "usps": [],
                "description": "<p>Europe's largest bus provider, "
                "witcross North and South America.</p>\r\n",
                "color": "#73D700",
                "color_light": "#E5F9C0",
                "color_dark": "#187D00",
            },
            "adf3cadd-7991-436c-be53-eb0f9c5ac165": {
                "name": "FlixTrain",
                "type": "core",
                "active": True,
                "logo": "https://cdn-cf.cms.flixbus.com/drupal-assets/2023-03/flixtrain-logo.png",
                "usps": [],
                "description": "<p>High-speed train routes across Germany and Sweden.</p>\r\n",
                "color": "#73D700",
                "color_light": "#E5F9C0",
                "color_dark": "#187D00",
            },
        },
        "cities": {
            "40d8f682-8646-11e6-9066-549f350fcb0c": {
                "name": "Berlin",
                "slug": "berlin",
                "legacy_id": 88,
                "id": "40d8f682-8646-11e6-9066-549f350fcb0c",
            },
            "40d9068f-8646-11e6-9066-549f350fcb0c": {
                "name": "Heidelberg",
                "slug": "heidelberg",
                "legacy_id": 98,
                "id": "40d9068f-8646-11e6-9066-549f350fcb0c",
            },
            "40d911c7-8646-11e6-9066-549f350fcb0c": {
                "name": "Düsseldorf",
                "slug": "duesseldorf",
                "legacy_id": 108,
                "id": "40d911c7-8646-11e6-9066-549f350fcb0c",
            },
            "40d917f9-8646-11e6-9066-549f350fcb0c": {
                "name": "Leipzig",
                "slug": "leipzig",
                "legacy_id": 113,
                "id": "40d917f9-8646-11e6-9066-549f350fcb0c",
            },
            "40d91e53-8646-11e6-9066-549f350fcb0c": {
                "name": "Hamburg",
                "slug": "hamburg",
                "legacy_id": 118,
                "id": "40d91e53-8646-11e6-9066-549f350fcb0c",
            },
            "40da4ac8-8646-11e6-9066-549f350fcb0c": {
                "name": "Hanover",
                "slug": "hannover",
                "legacy_id": 146,
                "id": "40da4ac8-8646-11e6-9066-549f350fcb0c",
            },
            "40db219f-8646-11e6-9066-549f350fcb0c": {
                "name": "Dresden",
                "slug": "dresden",
                "legacy_id": 355,
                "id": "40db219f-8646-11e6-9066-549f350fcb0c",
            },
            "40dde3b8-8646-11e6-9066-549f350fcb0c": {
                "name": "Amsterdam",
                "slug": "amsterdam",
                "legacy_id": 1334,
                "id": "40dde3b8-8646-11e6-9066-549f350fcb0c",
            },
            "40de1ad1-8646-11e6-9066-549f350fcb0c": {
                "name": "Prague",
                "slug": "prague",
                "legacy_id": 1374,
                "id": "40de1ad1-8646-11e6-9066-549f350fcb0c",
            },
            "40de8964-8646-11e6-9066-549f350fcb0c": {
                "name": "Paris",
                "slug": "paris",
                "legacy_id": 2015,
                "id": "40de8964-8646-11e6-9066-549f350fcb0c",
            },
            "40e07fbc-8646-11e6-9066-549f350fcb0c": {
                "name": "Eindhoven",
                "slug": "eindhoven",
                "legacy_id": 5078,
                "id": "40e07fbc-8646-11e6-9066-549f350fcb0c",
            },
        },
        "stations": {
            "dcbaaee6-9603-11e6-9066-549f350fcb0c": {
                "id": "dcbaaee6-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 1,
                "name": "Berlin central bus station",
                "slug": "berlin-zob",
                "is_train": False,
                "importance": 100,
            },
            "dcbac076-9603-11e6-9066-549f350fcb0c": {
                "id": "dcbac076-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 14,
                "name": "Heidelberg",
                "slug": "heidelberg",
                "is_train": False,
                "importance": 99,
            },
            "dcbaca96-9603-11e6-9066-549f350fcb0c": {
                "id": "dcbaca96-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 25,
                "name": "Düsseldorf",
                "slug": "dsseldorf",
                "is_train": False,
                "importance": 99,
            },
            "dcbad0e0-9603-11e6-9066-549f350fcb0c": {
                "id": "dcbad0e0-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 30,
                "name": "Leipzig central station",
                "slug": "leipzig",
                "is_train": False,
                "importance": 100,
            },
            "dcbada9a-9603-11e6-9066-549f350fcb0c": {
                "id": "dcbada9a-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 36,
                "name": "Hamburg ZOB",
                "slug": "hamburg",
                "is_train": False,
                "importance": 98,
            },
            "dcbb2109-9603-11e6-9066-549f350fcb0c": {
                "id": "dcbb2109-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 64,
                "name": "Hanover central bus station",
                "slug": "hannover",
                "is_train": False,
                "importance": 99,
            },
            "dcbb994f-9603-11e6-9066-549f350fcb0c": {
                "id": "dcbb994f-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 481,
                "name": "Berlin Südkreuz",
                "slug": "berlin-sdkreuz",
                "is_train": False,
                "importance": 80,
            },
            "dcbc6452-9603-11e6-9066-549f350fcb0c": {
                "id": "dcbc6452-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 1494,
                "name": "Prague (Central Bus Station Florenc)",
                "slug": "prag",
                "is_train": False,
                "importance": 99,
            },
            "dcbdd1b1-9603-11e6-9066-549f350fcb0c": {
                "id": "dcbdd1b1-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 2715,
                "name": "Amsterdam Sloterdijk",
                "slug": "amsterdam",
                "is_train": False,
                "importance": 100,
            },
            "dcbfd6bc-9603-11e6-9066-549f350fcb0c": {
                "id": "dcbfd6bc-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 3288,
                "name": "Berlin Alt-Tegel",
                "slug": "berlin-u-alt-tegel",
                "is_train": False,
                "importance": 40,
            },
            "dcc15c7e-9603-11e6-9066-549f350fcb0c": {
                "id": "dcc15c7e-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 5788,
                "name": "Eindhoven",
                "slug": "eindhoven",
                "is_train": False,
                "importance": 0,
            },
            "dcc5426b-9603-11e6-9066-549f350fcb0c": {
                "id": "dcc5426b-9603-11e6-9066-549f350fcb0c",
                "legacy_id": 11558,
                "name": "Paris (Bercy Seine)",
                "slug": "paris-bercy",
                "is_train": False,
                "importance": 100,
            },
            "d73477d0-4b42-44f5-9593-037c4b0b6e11": {
                "id": "d73477d0-4b42-44f5-9593-037c4b0b6e11",
                "legacy_id": 13328,
                "name": "Berlin Wannsee",
                "slug": "berlin-wannsee",
                "is_train": False,
                "importance": 0,
            },
            "394a5408-d778-4959-a63e-973253443ed2": {
                "id": "394a5408-d778-4959-a63e-973253443ed2",
                "legacy_id": 20688,
                "name": "Berlin Central Station (FlixTrain)",
                "slug": "berlin-central-station-train",
                "is_train": True,
                "importance": 95,
            },
            "895f31c8-7f88-4d8f-a070-4b4a6320160a": {
                "id": "895f31c8-7f88-4d8f-a070-4b4a6320160a",
                "legacy_id": 20788,
                "name": "Berlin Südkreuz (FlixTrain)",
                "slug": "berlin-sdkreuz-station-train",
                "is_train": True,
                "importance": 96,
            },
            "e6f7f0f4-4bb5-45a0-bcc2-d5e7279686dd": {
                "id": "e6f7f0f4-4bb5-45a0-bcc2-d5e7279686dd",
                "legacy_id": 20798,
                "name": "Berlin-Spandau (FlixTrain)",
                "slug": "berlin-spandau-station-train",
                "is_train": True,
                "importance": 80,
            },
            "9dc244f1-63d4-4db1-afbd-a10cc0377464": {
                "id": "9dc244f1-63d4-4db1-afbd-a10cc0377464",
                "legacy_id": 20818,
                "name": "Paris (Saint-Denis University)",
                "slug": "paris-saint-denis-universit",
                "is_train": False,
                "importance": 0,
            },
            "17483554-a4a8-4dad-b940-b5f56740014f": {
                "id": "17483554-a4a8-4dad-b940-b5f56740014f",
                "legacy_id": 44061,
                "name": "Berlin Airport BER, T 1/2",
                "slug": "berlin-airport-ber-p5",
                "is_train": False,
                "importance": 0,
            },
            "a3b04e6c-8c21-464a-81c0-d823066ffdf2": {
                "id": "a3b04e6c-8c21-464a-81c0-d823066ffdf2",
                "legacy_id": 100133,
                "name": "Dresden busparking Ammonstr.",
                "slug": "dresden-busparkplatz-ammonstrasse-ersatzhalt-dresden-hbf",
                "is_train": False,
                "importance": 0,
            },
        },
        "no_bikes_period": {},
    }
