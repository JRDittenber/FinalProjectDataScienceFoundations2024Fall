import sys
import os
import pymongo
from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging
from Primary_Folder.constants import DATABASE_NAME, MONGODB_URL

class MongoDBClient:
    """
    Class Name :   MongoDBClient
    Description :  This class connects to the MongoDB database and provides a client instance.
    
    Output      :  Connection to MongoDB database
    On Failure  :  Raises an exception
    """
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv("MONGODB_URL")
                if mongo_db_url is None:
                    raise Exception(f"Environment key: MONGODB_URL is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
                logging.info("MongoDB client initialized successfully.")
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info(f"Connected to MongoDB database: {database_name}")
        except Exception as e:
            logging.error(f"Error while connecting to MongoDB: {str(e)}")
            raise final_except(e, sys)






if __name__ == "__main__":
    try:
        mongo_client = MongoDBClient()
        print("MongoDB connection successful")
    except Exception as e:
        print(f"Error: {e}")
