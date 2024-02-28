import unittest
import pandas as pd
import os
import sys
import mongomock
from unittest import mock

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app import porsche_finder

class TestPorscheFinder(unittest.TestCase):
    def setUp(self):
        with mock.patch('pymongo.MongoClient', new=mongomock.MongoClient):
            self.finder = porsche_finder('test/test.ini', 'test/test.log')
        
        self.assertIsNotNone(self.finder.db, "Database should be initialized.")
        self.finder.reset_db()


    def test_setup(self):
        self.finder.setup()
        old_records = self.finder.db.retrieve_old()
        new_records = self.finder.db.retrieve_new()
        self.assertTrue(len(old_records) > 0, "Old listing records should not be empty.")
        self.assertTrue(len(new_records) > 0, "New listing records should not be empty.")

    def test_data_preparation(self):
        # test prep data prep data function is returning correct data type
        self.finder.setup()
        df_old, df_new = self.finder.prep_data()
        self.assertIsInstance(df_old, pd.DataFrame, "Old listings should be a DataFrame.")
        self.assertIsInstance(df_new, pd.DataFrame, "New listings should be a DataFrame.")

    def test_model_run(self):
        # test integration between data prep and model funcitons
        self.finder.setup()
        df_old, df_new = self.finder.prep_data()
        df_predicted = self.finder.run_model(df_old, df_new)
        self.assertIsInstance(df_predicted, pd.DataFrame, "Model output should be a DataFrame.")
        self.assertTrue("price" in df_predicted.columns, "Return from prediction function should have a price column.")

    def tearDown(self):
        # Clean up after tests
        self.finder.reset_db()

if __name__ == '__main__':
    unittest.main()
