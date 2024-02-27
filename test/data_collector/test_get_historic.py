import unittest
from unittest.mock import patch
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

from components.data_collector.get_historic import responseFetcher


class TestResponseFetcher(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.ini_file = os.path.join(current_dir, '..', 'test.ini')
        self.log_file = os.path.join(current_dir, '..', 'test.log')
        self.fetcher = responseFetcher(self.ini_file, self.log_file)

    @patch('components.data_collector.get_historic.requests.post')
    def test_fetch_response(self, mock_post):
        # Mock the response from requests.post
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "stats": {
                "sold": [{"id": "70050995", "title": "34k-Mile 2006 Porsche 911 Carrera 4S Coupe 6-Speed", "url": "https://bringatrailer.com/listing/2006-porsche-911-carrera-4s-coupe-16/", "image": "https://bringatrailer.com/wp-content/uploads/2024/01/2006_porsche_911-carrera-4s-coupe_2006_porsche_911-carrera-4s-coupe_6200c02a-64e9-401c-8add-f157b32661c5-af9rpy-68595-80830.jpg?resize=155%2C105", "amount": "46500"}],
                "unsold": []
            }
        }

        data = self.fetcher.fetch_response()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['_id'], '70050995')
        self.assertEqual(data[0]['title'], '34k-Mile 2006 Porsche 911 Carrera 4S Coupe 6-Speed')
        self.assertEqual(data[0]['url'], 'https://bringatrailer.com/listing/2006-porsche-911-carrera-4s-coupe-16/')
        self.assertEqual(data[0]['image_url'], 'https://bringatrailer.com/wp-content/uploads/2024/01/2006_porsche_911-carrera-4s-coupe_2006_porsche_911-carrera-4s-coupe_6200c02a-64e9-401c-8add-f157b32661c5-af9rpy-68595-80830.jpg?resize=155%2C105')
        self.assertEqual(data[0]['price'], '46500')

    def test_parse_listings(self):
        listings = [{"id": "70187902", "title": "2007 Porsche 911 Targa 4 6-Speed", "url": "https://bringatrailer.com/listing/2007-porsche-911-targa-4-6/", "image": "https://bringatrailer.com/wp-content/uploads/2024/01/2007_porsche_911-targa-4_2007_porsche_911-targa-4_3c5c286c-1978-47e6-b9e0-e3bf3e776781-dxsnml-50022-91354.jpg?resize=155%2C105", "amount": "37977"}]
        parsed_data = self.fetcher.parse_listings(listings)
        self.assertEqual(len(parsed_data), 1)
        self.assertEqual(parsed_data[0]['_id'], '70187902')
        self.assertEqual(parsed_data[0]['title'], '2007 Porsche 911 Targa 4 6-Speed')
        self.assertEqual(parsed_data[0]['url'], 'https://bringatrailer.com/listing/2007-porsche-911-targa-4-6/')
        self.assertEqual(parsed_data[0]['image_url'], 'https://bringatrailer.com/wp-content/uploads/2024/01/2007_porsche_911-targa-4_2007_porsche_911-targa-4_3c5c286c-1978-47e6-b9e0-e3bf3e776781-dxsnml-50022-91354.jpg?resize=155%2C105')
        self.assertEqual(parsed_data[0]['price'], '37977')

if __name__ == '__main__':
    unittest.main()
