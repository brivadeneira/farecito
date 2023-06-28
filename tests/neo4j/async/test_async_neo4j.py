"""
Implements async tests for Neo4j-based data models.
"""

import asyncio
from unittest.async_case import IsolatedAsyncioTestCase

import pytest

from tests.neo4j import Neo4JConnFactory


class Neo4jConnTests(IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, mocker):
        self.mocker = mocker

    @pytest.mark.asyncio
    async def test_init_driver_when_connection(self):
        driver_mock = self.mocker.patch("neo4j.AsyncGraphDatabase.driver", autospec=True)
        neo4j_conn = Neo4JConnFactory()
        driver_mock.assert_called_once_with(
            neo4j_conn.uri,
            auth=(neo4j_conn.user_name, neo4j_conn.password),
            database=neo4j_conn.db_name,
        )

    @pytest.mark.asyncio
    async def test_force_init_driver(self):
        driver_mock = self.mocker.patch("neo4j.AsyncGraphDatabase.driver", autospec=True)
        neo4j_conn = Neo4JConnFactory()
        neo4j_conn.init_driver()
        driver_mock.assert_called_with(
            neo4j_conn.uri,
            auth=(neo4j_conn.user_name, neo4j_conn.password),
            database=neo4j_conn.db_name,
        )
        self.assertEqual(driver_mock.call_count, 2)

    @pytest.mark.asyncio
    async def test_execute_query(self):
        driver_cls_mock = self.mocker.patch("neo4j.AsyncGraphDatabase.driver", autospec=True)

        neo4j_conn = Neo4JConnFactory()
        fake_query = "fake_query"
        _ = await neo4j_conn.execute_query(fake_query)
        driver_cls_mock.assert_called_with(
            neo4j_conn.uri,
            auth=(neo4j_conn.user_name, neo4j_conn.password),
            database=neo4j_conn.db_name,
        )

        driver_mock = driver_cls_mock.return_value  # driver()
        session_mock = driver_mock.session()
        session_mock.__aenter__.assert_awaited_once()

        session_mock.__aexit__.assert_awaited_once()
        # TODO add calls mock assertions
        # session_mock calls are:
        # [call.run('fake_query'),
        #  call.run().data(),
        #  call.run().data().__bool__(),
        #  call.run().data().__str__()]
        # and they are right! but next lines must to be defined:
        # session_run_mock = session_mock
        # session_run_mock.assert_awaited_once_with(fake_query)
        # assert res is session_executor_mock.return_value


# TODO add more tests
# TODO solve 'PytestUnknownMarkWarning: Unknown pytest.mark.asyncio - is this a typo?'


if __name__ == "__main__":
    asyncio.run(pytest.main(["-v"]))
