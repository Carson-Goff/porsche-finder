import pandas as pd
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
        self.preprocessor = None
        self.reg = None

    def setup_logging(self, log_file: str):
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger.info('Initialized logging.')

    def data_preprocessor(self, df):
        # transform dataframe to make it play nice with sklearn modeling
        df['year'] = pd.to_numeric(df['year'], errors='coerce').bfill()
        df['price'] = pd.to_numeric(df['price'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce').fillna(0)

        X = df[['year', 'trim', 'transmission', 'bodystyle']]
        y = df['price']
        
        categorical_features = ['trim', 'transmission', 'bodystyle']
        numeric_features = ['year']

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', 'passthrough', numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ])

        X_processed = self.preprocessor.fit_transform(X)
        return X_processed, y

    def train_model(self, df):
        # trains linear regression model on historical data
        X_processed, y = self.data_preprocessor(df)
        X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.3, random_state=42)

        self.reg = LinearRegression()
        self.reg.fit(X_train, y_train)

        score = self.reg.score(X_test, y_test)
        self.logger.info(f"The score of the model is: {score}")

    def predict_new_listings(self, df):
        # uses the trained model to predict prices of new listings
        if self.preprocessor is None or self.reg is None:
            raise Exception("The model has not been trained and the preprocessor is not available.")
        
        X_new = self.preprocessor.transform(df[['year', 'trim', 'transmission', 'bodystyle']])
        predicted_prices = [int(p) for p in self.reg.predict(X_new)]
        df['predicted'] = predicted_prices
        self.logger.info(f"Predicted prices: {predicted_prices}")
        return df

