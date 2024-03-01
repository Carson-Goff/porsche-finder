import requests
import configparser
import os
import logging

class responseFetcher:
    def __init__(self, ini_file, log_file):
        self.ini_file = ini_file
        self.log_file = log_file
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

        if os.path.exists(self.ini_file):
            self.config.read(self.ini_file)
            self.url = self.config['params']['url']
            
        # giant curl command to fetch data from the website. I'm sorry this is hardcoded, I dont like it either.
        self.url = "https://bringatrailer.com/wp-json/bringatrailer/1.0/data/listings-filter"
        self.headers = {
            "authority": "bringatrailer.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9,ru;q=0.8",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://bringatrailer.com",
            "referer": "https://bringatrailer.com/porsche/997-911/",
            "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        self.data = {
            "page": "1",
            "per_page": "24",
            "get_items": "1",
            "get_stats": "0",
            "base_filter[keyword_pages][]": "1833041",
            "base_filter[items_type]": "model",
            "sort": "td"
        }

        
    def setup_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
    def parse_listings(self, listings):
        # parses response to seperate listings into individual records
        self.logger.info('Parsing listings')
        extracted_data = []

        for listing in listings:
            data = {
                '_id': listing.get('id', None),
                'title': listing.get('title', None),
                'url': listing.get('url', None),
                'image_url': listing.get('image', None),
                'price': listing.get('amount', None)
            }

            extracted_data.append(data)

        return extracted_data

    def fetch_response(self):
        # sends the request and runs the parse_listings function to return a json
        response = requests.post(self.url, headers=self.headers, data=self.data)
        self.logger.info(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            response_json = response.json()
            self.logger.debug(f"Response status code: {response_json}")
        else:
            return f"Failed to fetch data: {response.status_code}"
        
        combined_entries = []
        sold_items = response_json.get("stats", {}).get("sold", [])
        combined_entries.extend(sold_items)
        unsold_items = response_json.get("stats", {}).get("unsold", [])
        combined_entries.extend(unsold_items)
        
        data = self.parse_listings(combined_entries)
        self.logger.info(data[0])

        return data
    
if __name__ == '__main__':
    data = responseFetcher.fetch_response()
    print(data)