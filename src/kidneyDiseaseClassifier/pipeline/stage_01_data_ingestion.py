from kidneyDiseaseClassifier.config.configuration import ConfigurationManager
from kidneyDiseaseClassifier.components.data_ingestion import DataIngestionGoogle, DataIngestionKaggle
from kidneyDiseaseClassifier import logger

STAGE_NAME = "Data Ingestion stage"


class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self, use_gdrive=False, use_kaggle=False):

        if use_gdrive and use_kaggle:
            raise ValueError("Use only on ata time")

        elif use_kaggle:
            try:
                config = ConfigurationManager()
                data_ingestion_config = config.get_data_ingestion_kaggle_config()
                data_ingestion = DataIngestionKaggle(config=data_ingestion_config)
                data_ingestion.download_kaggle_data()
                data_ingestion.extractor()
            except Exception as e:
                raise e

        elif use_gdrive:
            try:
                config = ConfigurationManager()
                data_ingestion_config = config.get_data_ingestion_gdrive_config()
                data_ingestion = DataIngestionGoogle(config=data_ingestion_config)
                data_ingestion.download_gdrive_data()
                data_ingestion.extractor()
            except Exception as e:
                raise e
        else:
            logger.info("No downloading choice has bee given")
            raise ValueError('Empty downloading choice!')


if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>> At stage {STAGE_NAME} started <<<<<<<<<")
        obj = DataIngestionTrainingPipeline()
        which_one = input("Inter your choice. Press g/G for Google, k/K, for kaggle")
        if which_one.lower() == 'k':
            logger.info(f"Downloading data from the kaggle")
            obj.main(use_kaggle=True)
        elif which_one.lower() == 'g':
            logger.info(f"Downloading data from the kaggle")
            obj.main(use_gdrive=True)
        logger.info(f">>>>>>>>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<\n\nx========================x\n\n")
    except Exception as e:
        logger.exception(e)
        raise e
