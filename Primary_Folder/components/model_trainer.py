import sys
from typing import Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from neuro_mf import ModelFactory

from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging
from Primary_Folder.utils.main import load_numpy_array_data, read_yaml_file, load_object, save_object
from Primary_Folder.entity.config_entity import ModelTrainerConfig
from Primary_Folder.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from Primary_Folder.entity.estimator import USVisaModel
from Primary_Folder.entity.estimator import TargetValueMapping


class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        """
        Initialize ModelTrainer with data transformation artifact and model trainer configuration.

        Args:
            data_transformation_artifact (DataTransformationArtifact): Output reference of data transformation artifact stage.
            model_trainer_config (ModelTrainerConfig): Configuration for model trainer.
        """
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train: np.array, test: np.array) -> Tuple[object, object]:
        """
        Get the best model object and report using neuro_mf.

        Args:
            train (np.array): Training data.
            test (np.array): Testing data.

        Returns:
            Tuple[object, object]: Metric artifact object and best model object.
        """
        try:
            logging.info("Using neuro_mf to get best model object and report")
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)

            x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]

            # Convert y_train and y_test to numerical values
            y_train = pd.Series(y_train).replace(TargetValueMapping()._asdict()).values
            y_test = pd.Series(y_test).replace(TargetValueMapping()._asdict()).values

            best_model_detail = model_factory.get_best_model(
                X=x_train, y=y_train, base_accuracy=self.model_trainer_config.expected_accuracy
            )
            model_obj = best_model_detail.best_model

            y_pred = model_obj.predict(x_test)

            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)

            return best_model_detail, metric_artifact

        except Exception as e:
            raise final_except(e, sys) from e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        Initiate the model trainer process.

        This function initiates all steps of the model trainer process and returns the model trainer artifact.

        Returns:
            ModelTrainerArtifact: The model trainer artifact with the training results.
        """
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        try:
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)

            best_model_detail, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)

            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")

            usvisa_model = USVisaModel(
                preprocessing_object=preprocessing_obj,
                trained_model_object=best_model_detail.best_model
            )
            logging.info("Created USVisa model object with preprocessor and model")
            logging.info("Created best model file path.")
            save_object(self.model_trainer_config.trained_model_file_path, usvisa_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact,
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise final_except(e, sys) from e
