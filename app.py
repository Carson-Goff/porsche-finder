import configparser
import sys
import os
import logging
import pandas as pd
import schedule
import time
from components.data_collector.db_ops import dbOperation
from components.data_collector.scrape_bat import dataCollector
from components.data_collector.get_historic import responseFetcher
from components.data_analyzer.transform_data import transform
from components.data_analyzer.model_history import model
from components.web_interface.web_app import app

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
        # sets up supporting directories then creates and populates database to be used by the application
        db_path = 'data/db'
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            self.logger.info(f"Created directory {db_path}")

        logs_path = 'logs'
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
            self.logger.info(f"Created directory {logs_path}")
            
        self.logger.info('Running application')
        self.db.setup_db()
        old = self.responseFetcher.fetch_response()
        print(f"Old records: {old}")
        # self.logger.info(f"Old Listings: {old}")
        new = self.collector.get_current_listings()
        print(f"New records: {new}")
        self.logger.info(new)
        self.db.insert_old_records(old)
        self.db.insert_new_records(new)

    def reset_db(self):
        # removes the database so it can be setup again in a clean state
        self.db.reset_db()
        
    def prep_data(self):
        # extracts fields from data to prepare it for the model
        old = pd.DataFrame(self.db.retrieve_old())
        new = pd.DataFrame(self.db.retrieve_new())
        df_old = self.transform.extract_fields(old)
        df_new = self.transform.extract_fields(new)
        
        return df_old, df_new
    
    def run_model(self, df_old, df_new):
        # trains the model and runs prediction on current listings
        self.model.train_model(df_old)
        df_new = self.model.predict_new_listings(df_new)
        
        return df_new
    
    def daily_job(self):
        # sets up actions into a single function so that the app can be refreshed daily
        self.reset_db()
        self.setup()
        df_old, df_new = self.prep_data()
        df2 = self.run_model(df_old, df_new)
        df2 = df2.astype({"year": int})

        if df2 is not None:
            app.config['DATAFRAME'] = df2
            app.run(debug=True)
        else:
            print("DataFrame is None, cannot start the server.")

def run_daily_job():
    if 'DYNO' in os.environ:
        # for when deployed on Heroku
        ini_file = 'heroku.ini'
    else:
        # for running locally
        ini_file = 'porsche-finder.ini'
    log_file = 'logs/porsche-finder.log'
    finder = porsche_finder(ini_file, log_file)
    finder.logger.info(os.environ)
    finder.daily_job()
    finder.logger.info("Daily run complete")

if __name__ == '__main__':
    run_daily_job()
    schedule.every().day.at("19:00").do(run_daily_job)
    while True:
        schedule.run_pending()
        time.sleep(60)
