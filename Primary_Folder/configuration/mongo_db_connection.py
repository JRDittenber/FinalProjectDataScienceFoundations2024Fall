import sys
import pymongo 
from pymongo import MongoClient

from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging 

import os 
from Primary_Folder.constants import DATABASE_NAME, MONGODB_URL


class MongoDB:
    
    """
    Class Name: export_data_into_feature_store
    Description: export data from MongoDB and store as a dataframe
    
    Output: connection to the database in Mongo
    On failure: raise exception
    """
    client = None 
    
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDB.client is None:
                mongo_db_url = os.getenv('MONGODB_DB_URL')
                if mongo_db_url is None:
                    raise Exception(f'Environment key: {MONGODB_URL} is required.')
                MongoDB.client = pymongo.MongoClient(mongo_db_url)
            self.client = MongoDB.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info('MongoDB connection successfully established')
        except Exception as e:
            raise final_except(e, sys)     
            


