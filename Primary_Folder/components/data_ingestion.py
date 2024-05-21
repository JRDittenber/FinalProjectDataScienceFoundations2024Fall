import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from Primary_Folder.entity.config_entity import DataIngestionConfig
from Primary_Folder.entity.artifact_entity import DataIngestionArtifact
from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging
from Primary_Folder.database_access.db_extract import VisaData


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        Initialize the DataIngestion class with a DataIngestionConfig.

        Args:
            data_ingestion_config (DataIngestionConfig, optional): Configuration for data ingestion.
                Defaults to DataIngestionConfig().
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise final_except(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export data from the database into the feature store.

        Returns:
            DataFrame: DataFrame containing exported data.
        """
        try:
            logging.info("Exporting data into feature store.")
            visa_data = VisaData()
            dataframe = visa_data.export_collection_as_df(
                collection_name=self.data_ingestion_config.collection_name
            )
            logging.info(f'Shape of the dataframe: {dataframe.shape}')

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving exported data into feature store at: {feature_store_file_path}")

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise final_except(e, sys)

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Split the data into training and testing sets.

        Args:
            dataframe (DataFrame): DataFrame to split.
        """
        logging.info("Entered split_data_as_train_test method of DataIngestion Class.")
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train-test split.")
            logging.info("Exited split_data_as_train_test method of DataIngestion Class.")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting training and test files.")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info("Exported training and test files.")
        except Exception as e:
            raise final_except(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiate the data ingestion component of the training pipeline.

        Returns:
            DataIngestionArtifact: Artifact containing paths to training and testing data.
        """
        logging.info("Entered initiate_data_ingestion method of Data Ingestion Class.")
        try:
            dataframe = self.export_data_into_feature_store()
            logging.info("Got the data from database.")
            self.split_data_as_train_test(dataframe)
            logging.info("Performed the train-test split.")
            logging.info("Exited initiate_data_ingestion method.")

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info(f'Data ingestion artifact: {data_ingestion_artifact}')
            return data_ingestion_artifact
        except Exception as e:
            raise final_except(e, sys) from e
