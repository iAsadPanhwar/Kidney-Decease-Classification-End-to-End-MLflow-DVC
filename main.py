from cnnClassifier.logger import logger
from cnnClassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from cnnClassifier.exception import CustomException
import sys


STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f">>>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<\n\nX============X")

except Exception as e:
    logger.exception(e)
    raise CustomException(e, sys)