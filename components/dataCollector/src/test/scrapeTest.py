import unittest
import requests_mock
from bs4 import BeautifulSoup
import os
import sys
import configparser

# Calculate the path to the root of the project ('web-app-test')
current_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory where the script is located
root_dir = os.path.join(current_dir, '/home/carson/software_architecture/applications/web-app-test/')  # Adjust the path to point to 'web-app-test'
sys.path.append(os.path.normpath(root_dir))  # Adds the project root directory to the Python path

from components.dataCollector.src.main.scrapeBat import dataCollector  # Import after adding project root to sys.path


class TestDataCollector(unittest.TestCase):

    def setUp(self):
        # Setup temporary INI file and log file
        self.ini_file = 'test_config.ini'
        self.log_file = 'test_log.log'
        self.test_url = 'http://example.com/'
        self.keywords = 'Porsche 911, Turbo'

        config = configparser.ConfigParser()
        config['params'] = {'url': self.test_url, 'keywords': self.keywords}
        with open(self.ini_file, 'w') as configfile:
            config.write(configfile)

        # Ensure the log file does not exist to start fresh
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def tearDown(self):
        # Cleanup by removing files created during tests
        os.remove(self.ini_file)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    @requests_mock.Mocker()
    def test_fetch_listings(self, m):
        # Mock the HTTP response
        mock_html = '<html><body><div class_="listing-card listing-card-separate"></div></body></html>'
        m.get(self.test_url, text=mock_html)

        collector = dataCollector(self.ini_file, self.log_file)
        soup = collector.fetch_listings()

        self.assertIsInstance(soup, BeautifulSoup, "The response should be a BeautifulSoup object")
        self.assertEqual(m.last_request.url, self.test_url, "The request URL should match the test URL")

    @requests_mock.Mocker()
    def test_parse_listings_new(self, m):
        # Prepare mock HTML and mock the HTTP response
        mock_html = '<html><body><div class_="listing-card listing-card-separate" data-listing_id="123"><h3><a href="http://example.com/listing">Title</a></h3><img src="http://example.com/image.jpg"/><span class_="bid-formatted">Price</span></div></body></html>'
        m.get(self.test_url, text=mock_html)

        collector = dataCollector(self.ini_file, self.log_file)
        soup = collector.fetch_listings()
        listings = collector.parse_listings(soup)

        self.assertIsInstance(listings, list, "The method should return a list")
        self.assertEqual(len(listings), 1, "There should be one listing parsed")
        self.assertEqual(listings[0]['title'], 'Title', "The title of the listing should be 'Title'")

    def test_log_listings(self):
        collector = dataCollector(self.ini_file, self.log_file)
        listings = [{'title': 'Test Listing', 'url': 'http://example.com/test'}]
        collector.log_listings(listings)

        # Check if log file has been updated correctly
        with open(self.log_file, 'r') as log_file:
            logs = log_file.readlines()

        self.assertTrue(len(logs) > 0, "The log file should contain entries")
        self.assertIn('Test Listing', logs[0], "The log should contain the listing title")

    # Additional methods can be added here to cover more functionalities

if __name__ == '__main__':
    unittest.main()
