import unittest
import mongomock
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

from components.data_collector.db_ops import dbOperation

class TestDbOperation(unittest.TestCase):

    def setUp(self):
        self.mock_client = mongomock.MongoClient()
        self.db_operation = dbOperation('test.ini', 'test.log')
        self.db_operation.myclient = self.mock_client
        self.db_operation.mydb = self.mock_client['test_db']
        self.db_operation.oldcol = self.db_operation.mydb['old_records']
        self.db_operation.newcol = self.db_operation.mydb['new_records']

    def test_insert_old_records(self):
        records = [{'item': 'old_record1'}, {'item': 'old_record2'}]
        self.db_operation.insert_old_records(records)
        self.assertEqual(self.db_operation.oldcol.count_documents({}), 2)

    def test_insert_new_records(self):
        records = [{'item': 'new_record1'}, {'item': 'new_record2'}]
        self.db_operation.insert_new_records(records)
        self.assertEqual(self.db_operation.newcol.count_documents({}), 2)

    def test_retrieve_old_records(self):
        self.db_operation.oldcol.insert_many([{'item': 'old_record1'}, {'item': 'old_record2'}])
        records = self.db_operation.retrieve_old()
        self.assertEqual(len(records), 2)

    def test_retrieve_new_records(self):
        self.db_operation.newcol.insert_many([{'item': 'new_record1'}, {'item': 'new_record2'}])
        records = self.db_operation.retrieve_new()
        self.assertEqual(len(records), 2)

if __name__ == '__main__':
    unittest.main()
