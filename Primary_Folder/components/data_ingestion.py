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
        Args:
            data_ingestion_config (DataIngestionConfig, optional): _description_. Defaults to DataIngestionConfig().
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise final_except(e, sys) 
    
    def  export_data_into_feature_store(self) -> DataFrame:
        """exports data from db into feature store

        Returns:
            DataFrame: containing exported data
        """
        try:
            logging.info("export_data_into_feature_store")
            visa_data = VisaData()
            dataframe = visa_data.export_collection_as_df(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f'Shape of the dataframe: {dataframe.shape}') 
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving exported data into feature store file path :{feature_store_file_path}")     
            dataframe.to_csv(feature_store_file_path, index = False, header = True)
            return dataframe
        except Exception as e:
            raise final_except(e, sys)
        
    def split_data_as_train_test(self, dataframe: DataFrame) -> None: 
        """split the data into train and test with the specified rato

        Args:
            dataframe (DataFrame): output S3 folder created  
        """
        logging.info("Entered split_data method of DataIngestion Class")
        
        try: 
            train_set, test_set = train_test_split(dataframe, test_size = self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split")
            logging.info("Exited split_data method of DataIngestion Class")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info("Exporting training and test file path")
            
            train_set.to_csv(self.data_ingestion_config.training_file_path, index = False, header = True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index = False, header = True)
            
            logging.info("Exported training and test file path")
        except Exception as e:
            raise final_except(e, sys)
        
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact: 
        """
        initiate the data ingestion compents of training pipeline
        
        train and test set are returned as artifacts of teh data ingestion components
        
        """    
        logging.info("Entered the initiate data ingestion method of Data Ingestion Class")
        
        try: 
            dataframe = self.export_data_into_feature_store()
            
            logging.info("Got the data from database")
            
            self.split_data_as_train_test(dataframe)
            
            logging.info("Performed the train and test split")
            
            logging.info("Exited initiate_data_ingestion method")
            
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f'Data ingestion artifact: {data_ingestion_artifact}')
            
            return data_ingestion_artifact
        except Exception as e:
            raise final_except(e, sys)            
            
                    