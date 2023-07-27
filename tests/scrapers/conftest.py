"""
This module contains fixtures for testing Scrapers.
"""

import pytest


@pytest.fixture
def flixbus_busstations_response_data_mock():
    # data_mock = MagicMock()
    # TODO [improvement] fake data generation
    data = {
        "took": 7,
        "timed_out": False,
        "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
        "hits": {
            "total": 3071,
            "max_score": None,
            "hits": [
                {
                    "_index": "cities_with_reachable_go-alt-1",
                    "_type": "doc",
                    "_id": "40de8964-8646-11e6-9066-549f350fcb0c:en-us",
                    "_score": None,
                    "_source": {
                        "name": "Paris",
                        "location": {"lon": 2.380503, "lat": 48.835334},
                        "id": 2015,
                        "search_volume": 6498100,
                        "uuid": "40de8964-8646-11e6-9066-549f350fcb0c",
                        "reachable": [
                            {
                                "id": 1965,
                                "uuid": "40de8463-8646-11e6-9066-549f350fcb0c",
                                "slug": "metz",
                            },
                            {
                                "id": 4468,
                                "uuid": "40e01d5a-8646-11e6-9066-549f350fcb0c",
                                "slug": "limoges",
                            },
                            {
                                "id": 4018,
                                "uuid": "40dff20a-8646-11e6-9066-549f350fcb0c",
                                "slug": "avignon",
                            },
                        ],
                        "sort": [6498100],
                    },
                },
                {
                    "_index": "cities_with_reachable_go-alt-1",
                    "_type": "doc",
                    "_id": "40d8f682-8646-11e6-9066-549f350fcb0c:en-us",
                    "_score": None,
                    "_source": {
                        "name": "Berlin",
                        "location": {"lon": 13.404616, "lat": 52.486081},
                        "id": 88,
                        "search_volume": 5894700,
                        "uuid": "40d8f682-8646-11e6-9066-549f350fcb0c",
                        "reachable": [
                            {
                                "id": 113,
                                "uuid": "40d917f9-8646-11e6-9066-549f350fcb0c",
                                "slug": "leipzig",
                            },
                            {
                                "id": 1394,
                                "uuid": "40de1f31-8646-11e6-9066-549f350fcb0c",
                                "slug": "wien",
                            },
                            {
                                "id": 7588,
                                "uuid": "40e19dd6-8646-11e6-9066-549f350fcb0c",
                                "slug": "lodz",
                            },
                        ],
                        "sort": [2822900],
                    },
                },
            ],
        },
    }
    # data_mock.__getitem__.side_effect = data.__getitem__
    # data_mock.__iter__.side_effect = data.__iter__
    return data
