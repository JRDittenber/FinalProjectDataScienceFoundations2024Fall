import os
import sys

import numpy as np
import pandas as pd
from pandas import DataFrame

from Primary_Folder.entity.config_entity import VisaPredictorConfig
from Primary_Folder.entity.s3_estimator import USvisaEstimator

from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging

from Primary_Folder.utils.main import read_yaml_file


class USVisaData:
    def __init__(self,
                 continent,
                 education_of_employee,
                 has_job_experience,
                 requires_job_training,
                 no_of_employees,
                 region_of_employment,
                 prevailing_wage,
                 unit_of_wage,
                 full_time_position,
                 company_age):
        """
        Initialize the USVisaData class with input data.
        """
        try:
            self.continent = continent
            self.education_of_employee = education_of_employee
            self.has_job_experience = has_job_experience
            self.requires_job_training = requires_job_training
            self.no_of_employees = no_of_employees
            self.region_of_employment = region_of_employment
            self.prevailing_wage = prevailing_wage
            self.unit_of_wage = unit_of_wage
            self.full_time_position = full_time_position
            self.company_age = company_age
        except Exception as e:
            raise final_except(e, sys) from e

    def get_usvisa_input_dataframe(self) -> DataFrame:
        """
        Convert the input data into a DataFrame.

        Returns:
            DataFrame: DataFrame containing the input data.
        """
        logging.info("Entered get_usvisa_input_dataframe method of USVisaData class")
        
        try:
            input_data = {
                "continent": [self.continent],
                "education_of_employee": [self.education_of_employee],
                "has_job_experience": [self.has_job_experience],
                "requires_job_training": [self.requires_job_training],
                "no_of_employees": [self.no_of_employees],
                "region_of_employment": [self.region_of_employment],
                "prevailing_wage": [self.prevailing_wage],
                "unit_of_wage": [self.unit_of_wage],
                "full_time_position": [self.full_time_position],
                "company_age": [self.company_age],
            }

            logging.info("Created USVisa data dictionary")
            logging.info("Exited get_usvisa_input_dataframe method of USVisaData class")

            return pd.DataFrame(input_data)
        except Exception as e:
            raise final_except(e, sys) from e


class USvisaClassifier:
    def __init__(self, prediction_pipeline_config: VisaPredictorConfig = VisaPredictorConfig()) -> None:
        """
        Initialize the USvisaClassifier with the prediction pipeline configuration.

        Args:
            prediction_pipeline_config (VisaPredictorConfig): Configuration for prediction.
        """
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise final_except(e, sys)

    def predict(self, dataframe: DataFrame) -> str:
        """
        Perform predictions on the given DataFrame.

        Args:
            dataframe (DataFrame): Input data for predictions.

        Returns:
            str: Predictions as a string.
        """
        try:
            logging.info("Entered predict method of USvisaClassifier class")
            model = USvisaEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result = model.predict(dataframe)
            return result
        except Exception as e:
            raise final_except(e, sys)
