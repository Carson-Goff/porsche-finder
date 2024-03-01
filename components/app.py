import configparser
import sys
import os
import logging
import pandas as pd
from .data_collector.db_ops import dbOperation
from .data_collector.scrape_bat import dataCollector
from .data_collector.get_historic import responseFetcher
from .data_analyzer.transform_data import transform
from .data_analyzer.model_history import model

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
            self.transform = transform(self.ini_file, self.log_file)
            self.model = model(self.ini_file, self.log_file)
            self.responseFetcher = responseFetcher(self.ini_file, self.log_file)
            
    def setup_logging(self):
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def setup(self):
        # Set up supporting directories then create and populate the database
        db_path = 'data/db'
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            self.logger.info(f"Created directory {db_path}")

        logs_path = 'logs'
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
            self.logger.info(f"Created directory {logs_path}")
            
        self.logger.info('Running application setup')
        self.db.setup_db()
        old_records = self.responseFetcher.fetch_response()
        new_records = self.collector.get_current_listings()
        # self.logger.info(f"Old records: {old_records}")
        self.logger.info(f"New records: {new_records}")
        self.db.insert_old_records(old_records)
        self.db.insert_new_records(new_records)

    def reset_db(self):
        # Remove the database to set it up again in a clean state
        self.db.reset_db()
        
    def prep_data(self):
        # Extract fields from data to prepare it for the model
        old_data = pd.DataFrame(self.db.retrieve_old())
        new_data = pd.DataFrame(self.db.retrieve_new())
        df_old = self.transform.extract_fields(old_data)
        df_new = self.transform.extract_fields(new_data)
        return df_old, df_new
    
    def run_model(self, df_old, df_new):
        # Train the model and predict on current listings
        self.model.train_model(df_old)
        df_new = self.model.predict_new_listings(df_new)
        return df_new
    
    def daily_job(self):
        # Sets up actions into a single function so that the app can be refreshed daily
        self.reset_db()
        self.setup()
        df_old, df_new = self.prep_data()
        df2 = self.run_model(df_old, df_new)
        if df2 is not None:
            df2 = df2.astype({"year": int})
            self.logger.info(f"DataFrame: {df2}")
            return df2
        else:
            self.logger.error("DataFrame is None, cannot start the server.")
            return None

def run_daily_job():
    ini_file = 'porsche-finder.ini'
    log_file = 'logs/porsche-finder.log'
    finder = porsche_finder(ini_file, log_file)
    df = finder.daily_job()
    finder.logger.info("Daily run complete")
    return df 

if __name__ == '__main__':
    df = run_daily_job()
    print(df)