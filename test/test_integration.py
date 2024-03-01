import unittest
import pandas as pd
import os
import sys
import mongomock
from unittest import mock

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from components.app import porsche_finder

class TestPorscheFinder(unittest.TestCase):
    @mock.patch('pymongo.MongoClient', new_callable=lambda: mongomock.MongoClient)
    def setUp(self, mock_mongo):
        self.finder = porsche_finder('test/test.ini', 'test/test.log')
        self.assertIsNotNone(self.finder.db, "Database should be initialized.")
        self.finder.reset_db()

    @mock.patch('pymongo.MongoClient', new_callable=lambda: mongomock.MongoClient)
    def test_setup(self, mock_mongo):
        self.finder.setup()
        old_records = self.finder.db.retrieve_old()
        new_records = self.finder.db.retrieve_new()
        self.assertGreater(len(old_records), 0, "Old listing records should not be empty.")
        self.assertGreater(len(new_records), 0, "New listing records should not be empty.")

    @mock.patch('pymongo.MongoClient', new_callable=lambda: mongomock.MongoClient)
    def test_data_preparation(self, mock_mongo):
        self.finder.setup()
        df_old, df_new = self.finder.prep_data()
        self.assertIsInstance(df_old, pd.DataFrame, "Old listings should be a DataFrame.")
        self.assertIsInstance(df_new, pd.DataFrame, "New listings should be a DataFrame.")

    @mock.patch('pymongo.MongoClient', new_callable=lambda: mongomock.MongoClient)
    def test_model_run(self, mock_mongo):
        self.finder.setup()
        df_old, df_new = self.finder.prep_data()
        df_predicted = self.finder.run_model(df_old, df_new)
        self.assertIsInstance(df_predicted, pd.DataFrame, "Model output should be a DataFrame.")
        self.assertIn("price", df_predicted.columns, "Return from prediction function should have a price column.")

    def tearDown(self):
        with mock.patch('pymongo.MongoClient', new=mongomock.MongoClient):
            self.finder.reset_db()

if __name__ == '__main__':
    unittest.main()
    