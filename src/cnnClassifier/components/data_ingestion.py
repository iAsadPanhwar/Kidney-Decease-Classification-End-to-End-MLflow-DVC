import os 
import zipfile
import gdown
from cnnClassifier.logger import logger
from cnnClassifier.utils.utils import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig
from cnnClassifier.exception import CustomException
import sys


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        
    def download_file(self) -> str:
        """
        Fetch the data from url
        """
        
        try: 
            dataset_url = self.config.source_URL
            zip_downlaod_dir = self.config.local_data_file
            os.makedirs("artifacts/data_ingestion", exist_ok = True)
            logger.info(f"Downloading data from {dataset_url} into file {zip_downlaod_dir}")
            
            file_id = dataset_url.split("/")[-2]
            prefix = "https://drive.google.com/uc?/export=download&id="
            gdown.download(prefix + file_id, zip_downlaod_dir)
            
            logger.info(f"Downlaoded data from {dataset_url} into file {zip_downlaod_dir}")
            
        except Exception as e:
            raise CustomException(e, sys)
        
    def extract_zip_file(self):
        
        """
        zip_file_path: str
        Extarcts the zip file into the data direcotry
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            