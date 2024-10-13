from cnnClassifier.constants import *
from cnnClassifier.utils.utils import read_yaml, create_directories
from cnnClassifier.exception import CustomException
import sys
from cnnClassifier.logger import logging
from cnnClassifier.entity.config_entity import DataIngestionConfig

class ConfigurationManager:
    
    """
    Manages the Configuration settings for the project.
    
    Reads the configurations form YAML files and sets up directories.
    """
    

    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):
        
        """
        Initialized the ConfigurationManager.
        
        Args:
            config_filepath (str): Path to the configuration YAML file.
            params_filepath (str): Path to the paramters YAML file
        """
        
        try:
            self.config = read_yaml(config_filepath)
            self.params = read_yaml(params_filepath)
        
        except Exception as e:
            logging.error(f"Failed to read YAML files: {e}")
            raise CustomException(e, sys)
        
        create_directories([self.config.artifacts_root])
        
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        
        """
        Retrieves and sets up the data ingestion configuration.
        
        Creates the necessary directories for data ingestion and returns a 
        DataIngestionConfig object containing configuration details.
        
        Returns:
            DataIngestionConfig: Configuration object for data ingestion.
        
        Raises:
            CustomException: If there is an error while creating directories.
        """
        
        try:
            config = self.config.data_ingestion
        
            create_directories([config.root_dir])
            data_ingestion_config = DataIngestionConfig(
                root_dir = config.root_dir,
                source_URL=config.source_URL,
                local_data_file=config.local_data_file,
                unzip_dir=config.unzip_dir
            )
            
            return data_ingestion_config

        except Exception as e:
            raise CustomException(e, sys)