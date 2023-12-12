import os
from kidneyDiseaseClassifier.constants import *
from kidneyDiseaseClassifier.utils.common import read_yaml, create_directories
from kidneyDiseaseClassifier.entity.config_entity import DataIngestionConfig, \
    PrepareBaseModelConfig, TrainingConfig, EvaluationConfig


class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.prams = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_gdrive_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion_gdrive

        create_directories([config.root_dir])

        data_ingestion_cfg = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            extracted_dir=config.extracted_dir
        )

        return data_ingestion_cfg

    def get_data_ingestion_kaggle_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion_kaggle

        create_directories([config.root_dir])

        data_ingestion_cfg = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            extracted_dir=config.extracted_dir
        )

        return data_ingestion_cfg


class PretrainModelConfigurationManager:
    def __init__(self, model_name="VGG16", config_filepath=CONFIG_FILE_PATH, params_file_path=PARAMS_FILE_PATH):
        self.model_name = model_name.upper()
        self.config = read_yaml(config_filepath)
        # loading params for the specific model
        self.params = read_yaml(params_file_path)[self.model_name]
        create_directories([self.config.artifacts_root])

    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        base_model_config = self.config.prepare_base_model
        # param = self.params[self.model]  # loading params for the specific model

        print("Config ---> ", base_model_config)
        print("Params --> ", self.params)

        create_directories([base_model_config.root_dir])
        prepared_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(base_model_config.root_dir),
            base_model_path=Path(base_model_config.base_model_path),
            updated_base_model_path=Path(
                base_model_config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_dropout_rate=self.params.DROPOUT_RATE,
            params_weights=self.params.WEIGHTS,
            params_include_top=self.params.INCLUDE_TOP,
            params_classes=self.params.CLASSES
        )

        return prepared_base_model_config

    def get_training_config(self) -> TrainingConfig:
        training = self.config.model_training
        prepare_base_model = self.config.prepare_base_model
        params = self.params

        training_data = os.path.join(self.config.data_ingestion_kaggle.local_data_file,
                                     "CT-KIDNEY-DATASET-Normal-Cyst-Tumor-Stone")
        create_directories([Path(training.root_dir)])

        # logger.info(f"training data path: {training_data}")
        # logger.info(f"{os.listdir(training_data)}")

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            updated_base_model_path=Path(
                prepare_base_model.updated_base_model_path),
            training_data=Path(training_data),
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE
        )

        return training_config

    def get_evaluation_config(self) -> EvaluationConfig:
        eval_config = EvaluationConfig(
            path_of_model= self.config.model_training.trained_model_path,
            training_data= "artifacts/data_ingestion/kaggle/data/CT-KIDNEY-DATASET-Normal-Cyst-Tumor-Stone",
            mlflow_uri= "https://dagshub.com/sadhiin/kidney-disease-classification-DL-MLOPS.mlflow",
            all_params=self.params,
            params_image_size=self.params.IMAGE_SIZE,
            params_batch_size=self.params.BATCH_SIZE
        )

        return eval_config
