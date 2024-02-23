import configparser
import os
import logging
import pandas as pd
from components.dataCollector.src.main.dbOps import dbOperation
from components.dataCollector.src.main.scrapeBat import dataCollector
from components.dataCollector.src.main.getHistoric import responseFetcher
from components.dataAnalyzer.src.main.transformData import transform
from components.dataAnalyzer.src.main.modelHistory import model

from components.webInterface.app import app

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
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
    def setup(self):
        self.logger.info('Running application')
        self.db.setup_db()
        old = self.responseFetcher.fetch_response()
        self.logger.info(f"Old Listings: {old}")
        new = self.collector.get_current_listings()
        self.logger.info(new)
        self.db.insert_old_records(old)
        self.db.insert_new_records(new)

    def reset_db(self):
        self.db.reset_db()
        
    def prep_data(self):
        old = pd.DataFrame(self.db.retrieve_old())
        new = pd.DataFrame(self.db.retrieve_new())
        old.to_csv('sampleData/old_listings.csv', index=False)
        new.to_csv('sampleData/new_listings.csv', index=False)
        df_old = self.transform.extract_fields(old)
        df_new = self.transform.extract_fields(new)
        
        return df_old, df_new
    
    def run_model(self, df_old, df_new):
        self.model.train_model(df_old)
        df_new = self.model.predict_new_listings(df_new)
        
        return df_new
        

if __name__ == '__main__':
    ini_file = 'porsche-finder.ini'
    log_file = 'logs/porsche-finder.log'
    finder = porsche_finder(ini_file, log_file)
    # finder.reset_db()
    # finder.setup()
    df_old, df_new = finder.prep_data()
    df2 = finder.run_model(df_old, df_new)
    df2 = df2.astype({"year": int})

    if df2 is not None:
        app.config['DATAFRAME'] = df2
        app.run(debug=True)
    else:
        print("DataFrame is None, cannot start the server.")
