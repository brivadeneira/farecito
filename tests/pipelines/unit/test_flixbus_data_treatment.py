"""
Implements tests for Scrapers models.
"""
import unittest
from datetime import datetime

import pytest

from pipelines.flixbus.bus_trips_pipeline import FlixbusTripsTracker
from pipelines.trip_alerts import TripsAlertBot
from tests.pipelines import FlixbusTripsTrackerFactory, TripsAlertBotFactory


class TestFlixbusTripsTracker(unittest.TestCase):
    def test_flixbus_trips_tracker(self):
        trips_tracker = FlixbusTripsTrackerFactory()
        self.assertIsInstance(trips_tracker, FlixbusTripsTracker)
        self.assertIsInstance(trips_tracker.discount_threshold, float)
        self.assertTrue(trips_tracker.discount_threshold < 1)


class TestTripAlertBot(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, test_cheap_trip):
        self.test_cheap_trip = test_cheap_trip

    def test_flixbus_alert_bot(self):
        test_cheap_trip = self.test_cheap_trip
        alert_bot = TripsAlertBotFactory(trip=test_cheap_trip)
        self.assertIsInstance(alert_bot, TripsAlertBot)
        self.assertIsNotNone(alert_bot.trip)
        self.assertIsInstance(alert_bot.trip, dict)
        self.assertEqual(
            alert_bot.ticket_url,
            "https://shop.flixbus.com/search?departureCity=40d8f682-8646-11e6-9066-549f350fcb0c"
            "%26arrivalCity=40de8964-8646-11e6-9066-549f350fcb0c%26rideDate=2024-07-26",
        )
        self.assertIsInstance(alert_bot.departure_date, str)
        self.assertEqual(alert_bot.departure_date, "2024-07-26")

        self.assertIsInstance(alert_bot.departure_date_time, datetime)
        self.assertEqual(
            alert_bot.departure_date_time,
            datetime.strptime("2024-07-26T00:00:00+0200", "%Y-%m-%dT%H:%M:%S%z"),
        )

        self.assertIsInstance(alert_bot.human_departure_date_time, str)
        self.assertEqual(alert_bot.human_departure_date_time, "Friday, July 26, 2024, 12:00 AM")

        message_strs = [
            "🎟 A cheap ticket for you!\n",
            "🚌 from Berlin to Paris\n",
            "💰 for just **2.98 EUROS**!",
            "\n📆 Schedule your next trip for 2024-07-26 00:00",
            "(11 months from now)",
            "GMT%2B2 time zone \n",
            "🏃 Hurry up! just **20 remaining seats**",
            "\n➡️ https://shop.flixbus.com/search?",
            "departureCity=40d8f682-8646-11e6-9066-549f350fcb0c",
            "%26arrivalCity=40de8964-8646-11e6-9066-549f350fcb0c",
            "%26rideDate=2024-07-26",
        ]
        for message_str in message_strs:
            self.assertIn(message_str, alert_bot.alert_message)

        # TODO [missing tests] add send alert test


class TestFlixbusCitiesDataGetter(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self):
        ...

    # TODO [missing tests]


if __name__ == "__main__":
    unittest.main()
