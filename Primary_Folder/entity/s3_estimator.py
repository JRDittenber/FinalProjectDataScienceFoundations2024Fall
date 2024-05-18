import sys
from pandas import DataFrame
from Primary_Folder.cloud_storage.aws_storage import SimpleStorageService
from Primary_Folder.exceptions import final_except
from Primary_Folder.entity.estimator import USVisaModel

class USvisaEstimator:
    """
    This class is used to save and retrieve US visa models in an S3 bucket and to make predictions.
    """

    def __init__(self, bucket_name: str, model_path: str):
        """
        Initialize the USvisaEstimator with the bucket name and model path.

        :param bucket_name: Name of your S3 bucket.
        :param model_path: Location of your model in the bucket.
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: USVisaModel = None

    def is_model_present(self, model_path: str) -> bool:
        """
        Check if the model is present in the specified path in the S3 bucket.

        :param model_path: Path of the model in the S3 bucket.
        :return: True if the model is present, False otherwise.
        """
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
        except final_except as e:
            print(e)
            return False

    def load_model(self) -> USVisaModel:
        """
        Load the model from the specified path in the S3 bucket.

        :return: The loaded USvisaModel.
        """
        try:
            return self.s3.load_model(self.model_path, bucket_name=self.bucket_name)
        except Exception as e:
            raise final_except(e, sys)

    def save_model(self, from_file: str, remove: bool = False) -> None:
        """
        Save the model to the specified path in the S3 bucket.

        :param from_file: Local path of the model file.
        :param remove: If True, remove the model file locally after uploading. Default is False.
        :return: None
        """
        try:
            self.s3.upload_file(from_file, to_filename=self.model_path, bucket_name=self.bucket_name, remove=remove)
        except Exception as e:
            raise final_except(e, sys)

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Make predictions on the given DataFrame using the loaded model.

        :param dataframe: Input data for predictions.
        :return: Predictions as a DataFrame.
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise final_except(e, sys)
