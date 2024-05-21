import sys

from Primary_Folder.cloud_storage.aws_storage import SimpleStorageService
from Primary_Folder.entity.artifact_entity import ModelPusherArtifact, ModelEvalutationArtifact
from Primary_Folder.entity.config_entity import ModelPusherConfig
from Primary_Folder.entity.s3_estimator import USvisaEstimator
from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging


class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvalutationArtifact,
                 model_pusher_config: ModelPusherConfig):
        """
        Initialize ModelPusher with model evaluation artifact and model pusher configuration.

        Args:
            model_evaluation_artifact (ModelEvalutationArtifact): Output reference of data evaluation artifact stage.
            model_pusher_config (ModelPusherConfig): Configuration for model pusher.
        """
        self.s3 = SimpleStorageService()
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.usvisa_estimator = USvisaEstimator(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.S3_model_key_path
        )

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Initiate the model pusher process.

        This function initiates all steps of the model pusher process, uploads the model
        to the specified S3 bucket, and returns the model pusher artifact.

        Returns:
            ModelPusherArtifact: The model pusher artifact containing bucket name and S3 model path.
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")

        try:
            logging.info("Uploading artifacts folder to S3 bucket")
            self.usvisa_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)

            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.S3_model_key_path
            )

            logging.info("Uploaded artifacts folder to S3 bucket")
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")

            return model_pusher_artifact
        except Exception as e:
            raise final_except(e, sys) from e
