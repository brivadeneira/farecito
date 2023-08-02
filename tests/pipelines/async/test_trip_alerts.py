"""
Test
"""
import asyncio
from unittest.async_case import IsolatedAsyncioTestCase

import pytest

from tests.pipelines import TripsAlertBotFactory


class TestTripAlertBot(IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, test_cheap_trip):
        self.test_cheap_trip = test_cheap_trip

    async def test_flixbus_alert_bot(self):
        test_cheap_trip = self.test_cheap_trip
        alert_bot = TripsAlertBotFactory(trip=test_cheap_trip)
        await alert_bot.send_alert_message()


if __name__ == "__main__":
    asyncio.run(pytest.main(["-v"]))
