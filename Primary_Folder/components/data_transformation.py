import sys 
import numpy as np 
import pandas as pd 

from sklearn.imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer


from Primary_Folder.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from Primary_Folder.entity.config_entity import DataTransformationConfig 
from Primary_Folder.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValdiationArtifact

from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging

from Primary_Folder.utils.main import save_object, save_numpy_array_data, read_yaml_file, drop_columns 
from Primary_Folder.entity.estimator import TargetValueMapping  

class DataTransformation: 
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, 
                 data_transformation_config: DataTransformationConfig, 
                 data_validation_artifact: DataValdiationArtifact):
        
        """output reference of data ingestion artifact, config for data transformation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise final_except(e, sys) 
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise final_except(e, sys)
        
    def get_data_transformer_object(self) -> Pipeline: 
        """creates and returns a Pipeline object
        """
        logging.info("Entered get_data_transformer_object method from DataTransformer class")
        
        try:
            logging.info("Got numerical cols from schema config")
            
