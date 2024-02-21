import pymongo
import os
import configparser
import logging
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, '/home/carson/software_architecture/applications/web-app-test/')
sys.path.append(os.path.normpath(root_dir))

from components.dataCollector.src.main.dbOps import dbOperation

data = dbOperation.retrieve_query({ "sold": False })
print(data)