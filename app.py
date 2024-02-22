import requests
from bs4 import BeautifulSoup
import datetime
import configparser
import os
import logging
import json
import re
import pandas as pd
from components.dataAnalyzer.src.main.modelHistory import model
from components.dataCollector.src.main.dbOps import dbOperation
from components.dataCollector.src.main.scrapeBat import dataCollector

class porsche_finder:
    
    def __init__(self, ini_file, log_file):
        self.ini_file = ini_file
        self.log_file = log_file
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

        if os.path.exists(self.ini_file):
            self.config.read(self.ini_file)
            self.db = dbOperation(self.ini_file, self.log_file)
            self.collector = dataCollector(self.ini_file, self.log_file)
            self.model = model(self.ini_file, self.log_file)
            
    def setup_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
    def setup(self):
        self.logger.info('Running application')
        self.db.setup_db()
        historic = self.collector.get_historic_listings()
        self.logger.info(historic)
        self.db.insert_record_list(historic)
        
    def get_data(self):
        data = self.db.retrieve_all()
        df = pd.DataFrame(data)
        print(df)
        titles = df['title'].tolist()
        print(titles)
        
        return df
        
    def test(self, df):
        df1 = self.model.extract_fields(df)
        print(df1)
        
        

if __name__ == '__main__':
    ini_file = 'porsche-finder.ini'
    log_file = 'logs/porsche-finder.log'
    finder = porsche_finder(ini_file, log_file)
    # finder.setup()
    df = finder.get_data()
    df1 = finder.test(df)