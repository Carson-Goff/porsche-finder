import pymongo
import os
import configparser
import logging
from typing import List


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
        # sets up mongodb and adds collections for new and old records
        mongo_client = self.config.get('database', 'mongo_client')
        db_name = self.config.get('database', 'db_name')
        self.myclient = pymongo.MongoClient(mongo_client)
        self.mydb = self.myclient[db_name]
        self.oldcol = self.mydb["sale_records"]
        self.newcol = self.mydb["new_records"]
        self.logger.info(self.myclient.list_database_names())
        
    def reset_db(self) -> None:
        # removes collections from the database so they can be reset
        mongo_client = self.config.get('database', 'mongo_client')
        db_name = self.config.get('database', 'db_name')
        self.myclient = pymongo.MongoClient(mongo_client)
        self.mydb = self.myclient[db_name]
        self.oldcol = self.mydb["sale_records"]
        self.newcol = self.mydb["new_records"]
        self.oldcol.drop()
        self.newcol.drop()

    def insert_old_records(self, records: List) -> None:
        self.oldcol.insert_many(records)
        
    def insert_new_records(self, records: List) -> None:
        self.newcol.insert_many(records)
        
    def retrieve_old(self) -> List:
        records = list(self.oldcol.find())
        
        return records
        
    def retrieve_new(self) -> List:
        records = list(self.newcol.find())
            
        return records
    