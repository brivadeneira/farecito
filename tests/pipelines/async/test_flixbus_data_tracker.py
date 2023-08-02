"""
Test
"""
import asyncio
from unittest.async_case import IsolatedAsyncioTestCase

import pytest

from pipelines.trip_alerts import TripsAlertBot
from tests.pipelines import FlixbusTripsTrackerFactory


class TestFlixbusBTripsTracker(IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, flixbus_trips_test_response):
        self.response_data = flixbus_trips_test_response

    async def test_flixbus_trips_tracker(self):
        trips_tracker = FlixbusTripsTrackerFactory()
        response_data = [self.response_data] * 2
        cheap_trips = await trips_tracker.track_data_of_interest(response_data)
        self.assertIsNotNone(cheap_trips)
        self.assertIsInstance(cheap_trips, list)
        self.assertEqual(len(cheap_trips), 24)

        for trip in cheap_trips:
            trip_alert_bot = TripsAlertBot(trip)
            await trip_alert_bot.send_alert_message()


if __name__ == "__main__":
    asyncio.run(pytest.main(["-v"]))
