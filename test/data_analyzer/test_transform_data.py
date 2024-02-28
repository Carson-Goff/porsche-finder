import unittest
import pandas as pd
import numpy as np
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

from components.data_analyzer.transform_data import transform

class test_transform(unittest.TestCase):

    def setUp(self):
        ini_file = os.path.join(current_dir, '..', 'test.ini')
        log_file = os.path.join(current_dir, '..', 'test.log')
        self.transform_instance = transform(ini_file, log_file)
        data = {
            'title': [
                '2007 Carrera Cabriolet',
                '2008 Carrera Coupe',
                '2012 Carrera GTS 6-Speed',
                '2011 Targa 4S 6-Speed'
                
            ],
            'price': ['$30,000', '$40,000', '$80,000', '$65,000']
        }
        self.df = pd.DataFrame(data)

    def test_extract_fields(self):
        transformed_df = self.transform_instance.extract_fields(self.df)
        self.assertEqual(len(transformed_df), len(self.df))
        self.assertTrue('year' in transformed_df.columns)
        self.assertTrue('trim' in transformed_df.columns)
        self.assertTrue('transmission' in transformed_df.columns)
        self.assertTrue('bodystyle' in transformed_df.columns)
        self.assertTrue(all(isinstance(year, int) for year in transformed_df['year']))
        self.assertTrue(all(isinstance(price, int) for price in transformed_df['price']))

if __name__ == '__main__':
    unittest.main()
