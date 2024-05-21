import sys
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from sklearn.metrics import f1_score

from Primary_Folder.constants import TARGET_COLUMN, CURRENT_YEAR
from Primary_Folder.entity.artifact_entity import (
    DataIngestionArtifact, 
    ModelEvalutationArtifact, 
    ModelTrainerArtifact
)
from Primary_Folder.entity.config_entity import ModelEvaluationConfig
from Primary_Folder.entity.estimator import TargetValueMapping, USVisaModel
from Primary_Folder.entity.s3_estimator import USvisaEstimator
from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float


class ModelEvaluation:

    def __init__(self, model_eval_config: ModelEvaluationConfig, data_ingestion_artifact: DataIngestionArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise final_except(e, sys) from e

    def get_best_model(self) -> Optional[USvisaEstimator]:
        """
        Get the best model currently in production, if available.
        
        Returns:
            USvisaEstimator: The best model in production, or None if no model is found.
        """
        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path = self.model_eval_config.S3_model_key_path
            usvisa_estimator = USvisaEstimator(bucket_name=bucket_name, model_path=model_path)

            if usvisa_estimator.is_model_present(model_path=model_path):
                return usvisa_estimator
            return None
        except Exception as e:
            raise final_except(e, sys)

    def evaluate_model(self) -> EvaluateModelResponse:
        """
        Evaluate the trained model against the best production model and choose the best one.
        
        Returns:
            EvaluateModelResponse: The evaluation result including f1 scores and acceptance status.
        """
        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            test_df['company_age'] = CURRENT_YEAR - test_df['yr_of_estab']

            x, y = test_df.drop(TARGET_COLUMN, axis=1), test_df[TARGET_COLUMN]
            y = y.replace(TargetValueMapping()._asdict())

            trained_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score

            best_model_f1_score = None
            best_model = self.get_best_model()
            if best_model is not None:
                y_hat_best_model = best_model.predict(x)
                best_model_f1_score = f1_score(y, y_hat_best_model)

            tmp_best_model_score = 0 if best_model_f1_score is None else best_model_f1_score
            result = EvaluateModelResponse(
                trained_model_f1_score=trained_model_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=trained_model_f1_score > tmp_best_model_score,
                difference=trained_model_f1_score - tmp_best_model_score
            )
            logging.info(f"Result: {result}")
            return result

        except Exception as e:
            raise final_except(e, sys)

    def initiate_model_evaluation(self) -> ModelEvalutationArtifact:
        """
        Initiate all steps of the model evaluation process.
        
        Returns:
            ModelEvalutationArtifact: The model evaluation artifact with the evaluation results.
        """
        try:
            evaluate_model_response = self.evaluate_model()
            s3_model_path = self.model_eval_config.S3_model_key_path

            model_evaluation_artifact = ModelEvalutationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                s3_model_path=s3_model_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_model_response.difference
            )

            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise final_except(e, sys) from e
