import requests
from bs4 import BeautifulSoup
import datetime
import configparser
import os
import logging
import json
import re

class dataCollector:
    def __init__(self, ini_file, log_file):
        self.ini_file = ini_file
        self.log_file = log_file
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

        if os.path.exists(self.ini_file):
            self.config.read(self.ini_file)
            self.url = self.config['params']['url']
            self.keywords = [item.strip() for item in self.config['params']['keywords'].split(',')]

    def setup_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def fetch_listings(self):
        self.logger.info('Fetching new listings')
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def parse_listings(self, soup, new=True):
        self.logger.info('Parsing listings')
        extracted_data = []

        if new:
            listings = soup.find_all('div', class_='listing-card listing-card-separate')
            for listing in listings:
                data = {
                    '_id': listing.get('data-listing_id', None),
                    'title': listing.find('h3').get_text(strip=True),
                    'url': listing.find('h3').find('a')['href'],
                    'image_url': listing.find('img')['src'] if listing.find('img') else None,
                    'price': listing.find('span', class_='bid-formatted').get_text(strip=True) if listing.find('span', class_='bid-formatted') else None,
                    'sold': None
                }
                extracted_data.append(data)
        else:
            script = soup.find('script', {'id': 'bat-theme-auctions-completed-initial-data'})
            if script and script.string:
                script_content = script.string
                json_start = script_content.find('{')
                json_end = script_content.rfind('}') + 1
                json_str = script_content[json_start:json_end]
                try:
                    data = json.loads(json_str)
                    listings = data.get('items', [])
                    for listing in listings:
                        sold = False
                        if 'Sold' in listing.get('sold_text', None):
                            sold = True
                        data = {
                            '_id': listing.get('id', None),
                            'title': listing.get('title', None),
                            'url': listing.get('url', None),
                            'image_url': listing.get('thumbnail_url', None),
                            'price': listing.get('current_bid_formatted', None),
                            'sold': sold
                        }
                        extracted_data.append(data)
                except json.JSONDecodeError as e:
                    self.logger.error(f'JSON decoding error: {e}')
                    return []

        return extracted_data


    def log_listings(self, listings):
        self.logger.info('Logging listings')
        with open(self.log_file, 'a') as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for listing in listings:
                file.write(f"{timestamp}: {listing['title']} - {listing['url']}\n")

    def run(self):
        soup = self.fetch_listings()
        # new_listings = self.parse_listings(soup)
        old_listings = self.parse_listings(soup, False)
        # print(*new_listings, sep='\n')
        print(*old_listings, sep='\n')

        # if new_listings:
        #     self.log_listings(new_listings)
        # else:
        #     print("No new listings found.")
    
    def get_historic_listings(self):
        soup = self.fetch_listings()
        old_listings = self.parse_listings(soup, False)
        
        return old_listings
        
    def get_current_listings(self):
        soup = self.fetch_listings()
        current_listings = self.parse_listings(soup)
        
        return current_listings

if __name__ == '__main__':
    ini_file = 'porsche-finder.ini'
    log_file = 'logs/porsche-finder.log'
    collector = dataCollector(ini_file, log_file)
    collector.run()
