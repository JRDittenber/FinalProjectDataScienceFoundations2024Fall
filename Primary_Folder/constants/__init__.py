import os
from datetime import date

DATABASE_NAME = 'FinalProjectSP24'
COLLECTION_NAME = 'VISA_DATA'
MONGO_URL = 'MONGO_URL'

PIPELINE_NAME: str = 'finalproject'
ARTIFACT_DIR: str = 'artifact'

MODEL_FILE_NAME = 'model.pkl'

TARGET_COLUMN = 'case_status'
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = 'preprocessing.pkl'

FILE_NAME: str = 'usvisa.csv'
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
AWS_DEFAULT_REGION = 'us-east-1'

# Data ingestion related constants
DATA_INGESTION_COLLECTION_NAME: str = 'VISA_DATA'
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_TRAIN_TRAIN_SPLIT: float = 0.2

# Data validation related constants
DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'data_drift'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'drift_report.yaml'

# Data transformation related constants
DATA_TRANSFORMATION_DIR_NAME: str = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = 'data_transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = 'data_transformed_object'

# Model trainer related constants
MODEL_TRAINER_DIR_NAME: str = 'model_trainer'
MODEL_TRAINER_TRAINED_DIR_NAME: str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME: str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")

MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_BUCKET_NAME = "usvisa-model2024rsc"
MODEL_PUSHER_S3_KEY = "model-registry"

APP_HOST = "0.0.0.0"
APP_PORT = 8080
