import configparser
import os
import logging
import pandas as pd
from components.dataCollector.src.main.dbOps import dbOperation
from components.dataCollector.src.main.scrapeBat import dataCollector
from components.dataAnalyzer.src.main.transformData import transform
from components.dataAnalyzer.src.main.modelHistory import model

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
            
    def setup_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
    def setup(self):
        self.logger.info('Running application')
        self.db.setup_db()
        historic = self.collector.get_historic_listings()
        self.logger.info(historic)
        self.db.insert_record_list(historic)

    
        
    def prep_model(self):
        data = self.db.retrieve_all()
        df = self.transform.extract_fields(pd.DataFrame(data))
        print(df)
        
        return df
    
    def run_model(self, df):
        self.model.train_model(df)

    def predict_prices(self):
        new = self.collector.get_current_listings()
        df2 = self.transform.extract_fields(pd.DataFrame(new))
        self.model.predict_new_listings(df2)
        
        

if __name__ == '__main__':
    ini_file = 'porsche-finder.ini'
    log_file = 'logs/porsche-finder.log'
    finder = porsche_finder(ini_file, log_file)
    # finder.setup()
    df = finder.prep_model()
    finder.run_model(df)
    finder.predict_prices()