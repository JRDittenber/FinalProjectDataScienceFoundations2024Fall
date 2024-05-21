import sys
from typing import Optional

import numpy as np
import pandas as pd

from Primary_Folder.configuration.mongo_db_connection import MongoDB
from Primary_Folder.constants import DATABASE_NAME
from Primary_Folder.exceptions import final_except


class VisaData:
    """
    This class is used to extract MongoDB data into a dataframe.
    """

    def __init__(self):
        """
        Initialize VisaData with a MongoDB connection.
        """
        try:
            self.mongo_client = MongoDB(database_name=DATABASE_NAME)
        except Exception as e:
            raise final_except(e, sys)

    def export_collection_as_df(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Export collection and return as a pandas DataFrame.

        Args:
            collection_name (str): Name of the MongoDB collection.
            database_name (Optional[str]): Name of the MongoDB database.

        Returns:
            pd.DataFrame: DataFrame containing the exported data.
        """
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise final_except(e, sys)
