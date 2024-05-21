import sys
import os
import pymongo

from Primary_Folder.constants import DATABASE_NAME, MONGODB_URL
from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging


class MongoDB:
    """
    Class Name: MongoDB
    Description: Export data from MongoDB and store it as a dataframe.
    
    Output: Connection to the MongoDB database.
    On failure: Raise an exception.
    """
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        """
        Initialize MongoDB connection.

        Args:
            database_name (str): Name of the database to connect to.
        """
        try:
            if MongoDB.client is None:
                mongo_db_url = os.getenv('MONGODB_URL')
                if mongo_db_url is None:
                    raise Exception(f'Environment key: {MONGODB_URL} is required.')
                MongoDB.client = pymongo.MongoClient(mongo_db_url)
            self.client = MongoDB.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info('MongoDB connection successfully established')
        except Exception as e:
            raise final_except(e, sys)
