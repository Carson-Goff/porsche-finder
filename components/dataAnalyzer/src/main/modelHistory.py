import pandas as pd
import numpy as np
import configparser
import logging
import os
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

class model:

    def __init__(self, ini_file: str, log_file: str):
        self.config = configparser.ConfigParser()
        if os.path.exists(ini_file):
            self.config.read(ini_file)
        else:
            raise FileNotFoundError(f"{ini_file} does not exist")
        
        self.logger = logging.getLogger(__name__)
        self.setup_logging(log_file)

    def setup_logging(self, log_file: str):
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger.info('Initialized logging.')
    

    def data_preprocessor(self, df):
        X = df[['year', 'trim', 'transmission', 'bodystyle']]
        y = df['price']

        categorical_features = ['trim', 'transmission', 'bodystyle']
        numeric_features = ['year']

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', 'passthrough', numeric_features),
                ('cat', OneHotEncoder(), categorical_features)
            ])
        
        X_processed = self.preprocessor.fit_transform(X)
        return X_processed, y

    def train_model(self, df):
        X_processed, y = self.data_preprocessor(df)
        print(X_processed)
        X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.3, random_state=42)

        self.reg = LinearRegression()
        self.reg.fit(X_train, y_train)

        score = self.reg.score(X_test, y_test)
        print(f"The score of the model is: {score}")
        self.logger.info(f"The score of the model is: {score}")


    def predict_new_listings(self, df):
        X_new, y = self.data_preprocessor(df)
        print(X_new)
        predicted_prices = [int(p) for p in self.reg.predict(X_new)]
        df['predicted'] = predicted_prices
        print(df)
        self.logger.info(f"Predicted prices: {predicted_prices}")

        return df
