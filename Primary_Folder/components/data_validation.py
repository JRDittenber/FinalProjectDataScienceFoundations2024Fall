import sys
import json

import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from pandas import DataFrame

from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging
from Primary_Folder.utils.main import read_yaml_file, write_yaml_file
from Primary_Folder.entity.artifact_entity import DataIngestionArtifact, DataValdiationArtifact
from Primary_Folder.entity.config_entity import DataValidationConfig
from Primary_Folder.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        """
        Initialize DataValidation with data ingestion artifact and data validation configuration.
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise final_except(e, sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        """
        Validate the number of columns in the dataframe.
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config['columns'])
            logging.info(f"The shape of the data is: [{status}]")
            return status
        except Exception as e:
            raise final_except(e, sys)

    def does_column_exist(self, df: DataFrame) -> bool:
        """
        Check if the columns exist in the dataframe.
        """
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            for column in self._schema_config['numerical_columns']:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if missing_numerical_columns:
                logging.info(f"The missing numerical columns are: {missing_numerical_columns}")

            for column in self._schema_config['categorical_columns']:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if missing_categorical_columns:
                logging.info(f"The missing categorical columns are: {missing_categorical_columns}")

            return not (missing_categorical_columns or missing_numerical_columns)
        except Exception as e:
            raise final_except(e, sys) from e

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise final_except(e, sys)

    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        """
        Validate if drift is detected.

        Returns:
            bool: Data drift status.
        """
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference_df, current_df)

            report = data_drift_profile.json()
            json_report = json.loads(report)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

            logging.info(f"{n_drifted_features}/{n_features} drift detected.")
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

            return drift_status
        except Exception as e:
            raise final_except(e, sys) from e

    def initiate_data_validation(self) -> DataValdiationArtifact:
        """
        Initiate the data validation component for the pipeline.

        Returns:
            DataValdiationArtifact: Artifact containing validation results.
        """
        try:
            validation_error_msg = ""
            logging.info("Entered the initiate data validation method of Data Validation Class")
            train_df, test_df = (
                DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            )

            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f'All required columns present in training data {status}')
            if not status:
                validation_error_msg += "Columns are missing from the training data"

            status = self.validate_number_of_columns(dataframe=test_df)
            logging.info(f'All required columns present in test data {status}')
            if not status:
                validation_error_msg += "Columns are missing from the test data"

            status = self.does_column_exist(df=train_df)
            if not status:
                validation_error_msg += "Columns are missing from the training data"

            status = self.does_column_exist(df=test_df)
            if not status:
                validation_error_msg += "Columns are missing from the test data"

            validation_status = len(validation_error_msg) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info("Drift detected")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logging.info(f"Validation error: {validation_error_msg}")

            data_validation_artifact = DataValdiationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info(f'Data validation artifact: {data_validation_artifact}')
            return data_validation_artifact
        except Exception as e:
            raise final_except(e, sys) from e
