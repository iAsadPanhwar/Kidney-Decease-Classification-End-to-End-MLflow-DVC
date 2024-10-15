from cnnClassifier.constants import *
from cnnClassifier.utils.utils import read_yaml, create_directories
from cnnClassifier.exception import CustomException
import sys
from cnnClassifier.logger import logger
from cnnClassifier.entity.config_entity import DataIngestionConfig, PrepareBaseModelConfig, TrainingConfig, EvaluationConfig
import os

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
            logger.error(f"Failed to read YAML files: {e}")
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
        

        
    def get_prepare_base_model(self) -> PrepareBaseModelConfig:
        """
        Retrieves and sets up the base model preparation configuration.

        Reads the base model preparation settings from the configuration file and creates
        necessary directories for storing the model files. Returns a PrepareBaseModelConfig
        object that includes paths and parameters for preparing the base model.

        Returns:
            PrepareBaseModelConfig: An object containing configurations for base model
                                    preparation, such as paths for saving the base model 
                                    and updated model, and training parameters like image size, 
                                    number of classes, and learning rate.

        Raises:
            CustomException: If there is an error while creating directories or accessing 
                             configuration parameters.
        """
        
        
        config = self.config.prepare_base_model
        
        create_directories([config.root_dir])
        
        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_classes=self.params.CLASSES,
            params_include_top=self.params.INCLUDE_TOP,
            params_learning_rate=self.params.LEARNING_RATE,
            params_weights=self.params.WEIGHTS
        )
        
        return prepare_base_model_config
    
    def get_training_config(self) -> TrainingConfig:
        """
        Retrieves and sets up the training configuration.

        Reads the training settings from the configuration file and creates the necessary
        directories for storing training results. It also sets up paths for training data 
        and the base model. Returns a TrainingConfig object that includes paths and parameters
        for model training.

        Returns:
            TrainingConfig: An object containing configurations for training the model,
                            such as paths for the trained model, updated base model, training
                            data, number of epochs, batch size, data augmentation flag, 
                            and image size.

        Raises:
            CustomException: If there is an error while creating directories or accessing 
                             configuration parameters.
        """

        
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        params = self.params
        training_data = os.path.join(self.config.data_ingestion.unzip_dir, "kidney-ct-scan-image")
        create_directories([
            Path(training.root_dir)
        ])
        
        training_config = TrainingConfig(
            root_dir = Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            updated_base_model_path=Path(prepare_base_model.updated_base_model_path),
            training_data = Path(training_data),
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE
        )
        
        return training_config
    
    def get_evaluation_config(self) -> EvaluationConfig:
        """
    Prepares and returns the evaluation configuration.

    This method sets up the configuration required for model evaluation. It specifies 
    paths to the trained model and training data, as well as details necessary for 
    connecting to the MLflow tracking server. It also retrieves essential parameters 
    such as image size and batch size for the evaluation process.

    Returns:
        EvaluationConfig: A data class containing all evaluation configuration settings, 
        including:
            - path_of_model (str): Path to the trained model file.
            - training_data (str): Path to the directory containing training data.
            - mlflow_uri (str): The URI for connecting to the MLflow tracking server.
            - all_params (ConfigBox): Contains all parameters from the params file.
            - params_image_size (tuple): Image size parameter for evaluation.
            - params_batch_size (int): Batch size parameter for evaluation.
    """
        eval_config = EvaluationConfig(
            path_of_model="artifacts/training/model.h5",
            training_data="artifacts/data_ingestion/kidney-ct-scan-image",
            mlflow_uri="https://dagshub.com/asadalipuh5/Kidney-Decease-Classification-End-to-End-MLflow-DVC.mlflow",
            all_params=self.params,
            params_image_size=self.params.IMAGE_SIZE,
            params_batch_size=self.params.BATCH_SIZE
        )

        return eval_config

        