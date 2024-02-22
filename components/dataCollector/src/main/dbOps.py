import pymongo
import os
import configparser
import logging
from typing import List, Dict


class dbOperation:
    
    def __init__(self, ini_file: str, log_file: str):
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger(__name__)
        self.setup_logging(log_file)

        if os.path.exists(ini_file):
            self.config.read(ini_file)
            self.setup_db()

    def setup_logging(self, log_file: str) -> None:
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def setup_db(self) -> None:
        # Assuming 'database' section and keys exist in your config file
        mongo_client = self.config.get('database', 'mongo_client')
        db_name = self.config.get('database', 'db_name')
        self.myclient = pymongo.MongoClient(mongo_client)
        self.mydb = self.myclient[db_name]
        self.mycol = self.mydb["past_sales"]
        self.logger.info(self.myclient.list_database_names())

    def insert_record_list(self, records: List) -> None:
        x = self.mycol.insert_many(records)
        self.logger.info(f"Record ID's inserted: {x.inserted_ids}")

    def retrieve_record(self):
        x = self.mycol.find_one()
        self.logger.info(f"Single record retrieved: {x}")
        
    def retrieve_all(self) -> List:
        mydoc = list(self.mycol.find())
        self.logger.info(f"Records retrieved: {mydoc}")
            
        return mydoc

    def retrieve_query(self, query: Dict):
        mydoc = self.mycol.find(query)
        self.logger.info(f"Records retrieved: {mydoc}")
            
        return mydoc
    

if __name__ == '__main__':
    ini_file = 'porsche-finder.ini'
    log_file = 'logs/porsche-finder.log'
    db = dbOperation(ini_file, log_file)
    db.setup_db()
    # db.refresh_historical()
    # db.retrieve_record()
    db.retrieve_query({ "sold": False })