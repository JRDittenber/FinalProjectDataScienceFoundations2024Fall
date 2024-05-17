from Primary_Folder.pipeline.traning_pipeline import TrainPipeline
from Primary_Folder.logger import logging
from Primary_Folder.exceptions import final_except
import sys
 
try:    
    pipeline = TrainPipeline()
    pipeline.run_pipeline()
except Exception as e:
    raise final_except(e, sys)

logging.info(sys)