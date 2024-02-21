import pymongo
import os
import sys
import configparser
import logging
from scrapeBat import dataCollector


class dbOperation:
    
    def __init__(self, ini_file, log_file):
        self.ini_file = ini_file
        self.log_file = log_file
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

        if os.path.exists(self.ini_file):
            self.config.read(self.ini_file)
            self.mongo_client = self.config['database']['mongo_client']
            self.db_name = self.config['database']['db_name']
            
    def setup_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def setup_db(self):
        myclient = pymongo.MongoClient(self.mongo_client)
        mydb = myclient[self.db_name]
        self.mycol = mydb["past_sales"]
        print(myclient.list_database_names())

    def insert_historical(self):
        collector = dataCollector(self.ini_file, self.log_file)
        historic_listings = collector.get_historic_listings()
        print(historic_listings)

        x = self.mycol.insert_many(historic_listings)
        print(x.inserted_ids)

    def retrieve_record(self):
        x = self.mycol.find_one()
        print(x)

    def retrieve_query(self):
        myquery = { "sold": False }
        mydoc = self.mycol.find(myquery)
        for x in mydoc:
            print(x)
    

if __name__ == '__main__':
    ini_file = 'porsche-finder.ini'
    log_file = 'logs/porsche-finder.log'
    db = dbOperation(ini_file, log_file)
    db.setup_db()
    # db.refresh_historical()
    # db.retrieve_record()
    db.retrieve_query()
