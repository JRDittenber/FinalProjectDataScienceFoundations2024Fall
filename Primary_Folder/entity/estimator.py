import sys
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging

class TargetValueMapping:
    def __init__(self):
        self.certified: int = 0
        self.denied: int = 1

    def as_dict(self):
        """Return the mapping as a dictionary."""
        return self.__dict__

    def reverse_mapping(self):
        """Return a dictionary with reversed key-value pairs."""
        mapping_response = self.as_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))

class USVisaModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        Initialize USVisaModel with a preprocessing pipeline and a trained model.

        Args:
            preprocessing_object (Pipeline): The preprocessing pipeline object.
            trained_model_object (object): The trained model object.
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Perform predictions on the given DataFrame.

        Args:
            dataframe (DataFrame): The input data for predictions.

        Returns:
            DataFrame: The predictions.

        Raises:
            final_except: Custom exception for handling errors.
        """
        logging.info("Entered the predict method of USVisaModel class")

        try:
            logging.info("Transforming the input data using the preprocessing pipeline")
            transformed_feature = self.preprocessing_object.transform(dataframe)
            logging.info("Using the trained model to get predictions")
            return self.trained_model_object.get_predictions(transformed_feature)
        except Exception as e:
            raise final_except(e, sys)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"

