import unittest
from unittest.mock import patch, MagicMock
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

from components.data_collector.scrape_bat import dataCollector

class TestDataCollector(unittest.TestCase):

    def setUp(self):
        ini_file = os.path.join(current_dir, '..', 'test.ini')
        log_file = os.path.join(current_dir, '..', 'test.log')
        self.collector = dataCollector(ini_file, log_file)

    @patch('components.data_collector.scrape_bat.requests.get')
    def test_fetch_listings(self, mock_get):
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = '<html></html>'
        soup = self.collector.fetch_listings()
        self.assertIsNotNone(soup)

    @patch('components.data_collector.scrape_bat.BeautifulSoup')
    def test_parse_listings(self, mock_soup):
        mock_soup.return_value.find_all.return_value = []
        listings = self.collector.parse_listings(mock_soup)
        self.assertIsInstance(listings, list)
        self.assertEqual(len(listings), 0)

    def test_log_listings(self):
        listings = [{'title': 'Test Listing', 'url': 'http://example.com'}]
        self.collector.log_listings(listings)

if __name__ == '__main__':
    unittest.main()
