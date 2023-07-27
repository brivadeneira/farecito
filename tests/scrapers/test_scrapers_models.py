"""
Implements tests for Scrapers models.

NOTE: Define a pytest fixture named __inject_fixtures with the autouse=True option is necessary,
 in order to inject the value of fixtures into all test methods in the test class where it is used.
"""
import unittest

from requests import Session

from scrapers import BaseScraper
from tests.scrapers import BaseScraperFactory


class TestBaseScraper(unittest.TestCase):
    def test_base_scraper(self):
        base_scraper = BaseScraperFactory()
        self.assertIsInstance(base_scraper, BaseScraper)

        self.assertIsInstance(base_scraper.endpoint_uris, list)
        self.assertIsInstance(base_scraper.retries, int)
        self.assertIsInstance(base_scraper.backoff, float)
        self.assertIsInstance(base_scraper.status_forcelist, tuple)
        self.assertIsInstance(base_scraper.timeout, int)
        self.assertIsInstance(base_scraper.requests_retry_session, (Session, type(None)))

    def test_invalid_endpoint_uri_value(self):
        with self.assertRaises(TypeError):
            BaseScraper(endpoint_uris=-3.1416)

    def test_build_headers(self):
        base_scraper = BaseScraperFactory()
        headers = base_scraper.build_headers()
        # TODO [missing tests] add call asserts
        expected_headers_keys = {"User-Agent", "Accept", "Connection"}
        self.assertEqual(set(headers.keys()), expected_headers_keys)
        for k in headers.keys():
            self.assertIsInstance(headers[k], str)

    # TODO [missing tests]
    """
    @patch('requests.Session')
    @patch('requests.adapters.HTTPAdapter')
    def test_requests_retry_session(self, http_adapter_mock, session_mock):
        session_instance_mock = session_mock.return_value
        http_adapter_instance_mock = http_adapter_mock.return_value
        retry_instance_mock = Mock()
        http_adapter_instance_mock.max_retries = retry_instance_mock

        base_scraper = BaseScraper(endpoint_url='http://dummy.url/dummy_endpoint')

        result = base_scraper.get_data()

        session_mock.assert_called_once()
        session_instance_mock.mount.assert_called_with('https://', http_adapter_instance_mock)
    """


if __name__ == "__main__":
    unittest.main()
