from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.components.data_ingestion import DataIngestion
from cnnClassifier.exception import CustomException
from cnnClassifier.logger import logger
import sys


STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config = data_ingestion_config)
            data_ingestion.download_file()
            data_ingestion.extract_zip_file()
    
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == 'main':
    try:
        logger.info(f">>>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<\n\nX============X")
    
    except Exception as e:
        logger.exception(e)
        raise CustomException(e, sys)
        