import sys 

from pandas import DataFrame
from sklearn.pipeline import Pipeline

from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging 

class TargetValueMapping:
    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1
    def _asdict(self):
        return self.__dict__
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))
    
    
    
class USVisaModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """input objects of preprocessor and trained model
        """
        self.preprocessing_object = preprocessing_object 
        self.trained_model_object = trained_model_object
        
    def predict(self, dataframe: DataFrame) -> DataFrame:
        """accepts raw input and then transforms the raw input into a preprocessing object which guarantees that
        the data is in the correct format for the model to be trained on.Peforms predictions on transformed data"      
        """
        logging.info("Entered the predict method of US Visa class")
        
        try:
            logging.info("Useing the trained model to get predictions")
            
            transformed_feature = self.preprocessing_object.transform(dataframe)
            logging.info("Using the trained model to get predictions")
            return self.trained_model_object.get_predictions(transformed_feature)
        except Exception as e:
            raise final_except(e, sys) 
        
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"
                         
        
        
            