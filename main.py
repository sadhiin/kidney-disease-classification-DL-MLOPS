from kidneyDiseaseClassifier import logger
from kidneyDiseaseClassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline

STAGE_NAME = "Data Ingestion Stage"
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
except Exception as e:
    logger.exception(e)
    raise e
