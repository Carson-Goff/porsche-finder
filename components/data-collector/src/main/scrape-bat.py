import requests
from bs4 import BeautifulSoup
import datetime
import configparser
import os
import logging
import sys
import json


def fetch_listings(url):
    logger = logging.getLogger()
    logger.info('Fetching new listings')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def parse_new_listings(soup):
    logger = logging.getLogger()
    logger.info('Fetching new listings')

    listings = soup.find_all('div', class_='listing-card listing-card-separate')

    extracted_data = []
    for listing in listings:
        data = {
            'listing_id': listing.get('data-listing_id', None),
            'title': listing.find('h3').get_text(strip=True),
            'url': listing.find('h3').find('a')['href'],
            'image_url': listing.find('img')['src'] if listing.find('img') else None,
            'price': listing.find('span', class_='bid-formatted').get_text(strip=True) if listing.find('span', class_='bid-formatted') else None
        }
        extracted_data.append(data)

    return extracted_data


def parse_old_listings(soup):
    logger = logging.getLogger()
    logger.info('Fetching new listings')

    script = soup.find('script', {'id': 'bat-theme-auctions-completed-initial-data'})
    script_content = script.string
    json_str = script_content.split('var auctionsCompletedInitialData = ')[1].split('/* ]]> */')[0].strip()
    print(json_str)
    listings = json.loads(json_str)

    extracted_data = []
    for listing in listings['items']:
        data = {
            'listing_id': listing.get('data-listing_id', None),
            'title': listing.find('h3').get_text(strip=True),
            'url': listing.find('h3').find('a')['href'],
            'image_url': listing.find('img')['src'] if listing.find('img') else None,
            'price': listing.find('span', class_='bid-formatted').get_text(strip=True) if listing.find('span', class_='bid-formatted') else None
        }
        extracted_data.append(data)

    return extracted_data



def extract_listing_details(listing):
    # Implement extraction logic based on the webpage's structure
    return {
        'title': 'Sample Title',  # Replace with actual data extraction logic
        'url': 'Sample URL'
    }

def log_listings(listings):
    logger = logging.getLogger()
    with open('porsche_997_911_log.txt', 'a') as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for listing in listings:
            file.write(f"{timestamp}: {listing['title']} - {listing['url']}\n")

if __name__ == '__main__':
    ini_file = 'porsche-finder.ini'
    log_file = 'logs/porsche-finder.log'
    config = configparser.ConfigParser()

    if os.path.exists(ini_file):
        config.read(ini_file)

        url = config['params']['url']
        keywords = config['params']['keywords']
        keywords = [item.strip() for item in keywords.split(',')]
        soup = fetch_listings(url)
        new_listings = parse_new_listings(soup)
        print(*new_listings, sep='\n')

        # old_listings = parse_old_listings(soup)
        # print(old_listings)
        # print(*old_listings, sep='\n')
        # if new_listings:
        #     log_listings(new_listings)
        # else:
        #     print("No new listings found.")