from Primary_Folder.configuration.mongo_db_connection import MongoDBClient
from Primary_Folder.constants import DATABASE_NAME
from Primary_Folder.exceptions import final_except
import pandas as pd
import sys
from typing import Optional
import numpy as np
import logging

class USvisaData:
    """
    This class helps to export the entire MongoDB record as a pandas dataframe.
    """

    def __init__(self):
        """
        Initializes the MongoDB client.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            logging.info("MongoDB client initialized successfully.")
        except Exception as e:
            raise final_except(e, sys)
        

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports the entire collection as a dataframe.
        :param collection_name: Name of the collection to export.
        :param database_name: Name of the database (optional).
        :return: pd.DataFrame of the collection.
        """
        try:
            logging.info(f"Exporting data from collection: {collection_name}")

            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            # Fetch data from MongoDB
            data = list(collection.find())
            logging.info(f"Number of records fetched: {len(data)}")

            df = pd.DataFrame(data)

            if df.empty:
                logging.warning(f"The dataframe for collection {collection_name} is empty.")
                return df

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
                logging.info("Dropped '_id' column from the dataframe.")

            df.replace({"na": np.nan}, inplace=True)
            logging.info(f"Dataframe shape after processing: {df.shape}")
            return df
        except Exception as e:
            raise final_except(e, sys)
