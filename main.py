from kidneyDiseaseClassifier import logger
from kidneyDiseaseClassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from kidneyDiseaseClassifier.pipeline.stage_02_prepare_base_model import PrepareBaseModelTrainingPipeline
from kidneyDiseaseClassifier.pipeline.stage_03_model_training import ModelTrainingPipeline

# STAGE_NAME = "Data Ingestion Stage"
#
# try:
#     logger.info(f">>>>>>>>> At stage {STAGE_NAME} started <<<<<<<<<")
#     obj = DataIngestionTrainingPipeline()
#     which_one = input("Inter your choice. Press 'g' or 'G' for Google, 'k' or 'K' for kaggle: ")
#     if which_one.lower() == 'k':
#         logger.info(f"Downloading data from the kaggle")
#         obj.main(use_kaggle=True)
#     elif which_one.lower() == 'g':
#         logger.info(f"Downloading data from the kaggle")
#         obj.main(use_gdrive=True)
# except Exception as e:
#     logger.exception(e)
#     raise e
#

STAGE_NAME = "Prepare base model"

try:
    logger.info("#####################################")
    logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<<<<<<<<")

    prepare_base_model = PrepareBaseModelTrainingPipeline()
    prepare_base_model.main()
    logger.info(f">>>>>>>>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<")

except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Training"

try:
    logger.info("#####################################")
    logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<<<<<<<<")
    obj = ModelTrainingPipeline()
    obj.main()
    logger.info(f">>>>>>>>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<\n\nx========================x\n\n")
except Exception as e:
    logger.exception(e)
    raise e
