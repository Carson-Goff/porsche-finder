import unittest
import pandas as pd
import numpy as np
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

from components.data_analyzer.model_history import model

class test_model_history(unittest.TestCase):

    def setUp(self):
        ini_file = os.path.join(current_dir, '..', 'test.ini')
        log_file = os.path.join(current_dir, '..', 'test.log')
        self.model_instance = model(ini_file, log_file)
        data = {
            'year': ['2007', '2008', '2012', '2011'],
            'trim': ['Carrera', 'Carrera', 'Carrera GTS', 'Targa 4S'],
            'transmission': ['A', 'A', 'M', 'M'],
            'bodystyle': ['Cabriolet', 'Coupe', 'Coupe', 'Targa'],
            'price': [30000, 40000, 80000, 65000]
        }
        self.df = pd.DataFrame(data)

    def test_data_preprocessor(self):
        X_processed, y = self.model_instance.data_preprocessor(self.df)
        self.assertEqual(X_processed.shape[0], len(self.df))
        self.assertTrue(np.all(y >= 0))

    def test_train_model(self):
        self.model_instance.train_model(self.df)
        self.assertIsNotNone(self.model_instance.reg)

    def test_predict_new_listings(self):
        self.model_instance.train_model(self.df)
        predictions = self.model_instance.predict_new_listings(self.df)
        self.assertEqual(len(predictions), len(self.df))
        self.assertIn('predicted', predictions.columns)

if __name__ == '__main__':
    unittest.main()
