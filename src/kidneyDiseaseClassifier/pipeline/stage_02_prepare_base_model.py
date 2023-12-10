from kidneyDiseaseClassifier import logger
from kidneyDiseaseClassifier.config.configuration import PretrainModelConfigurationManager
from kidneyDiseaseClassifier.components.prepare_base_model import PrepareBaseModel


STAGE_NAME = "Prepare base model"


class PrepareBaseModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = PretrainModelConfigurationManager('VGG16')
            prepare_base_model_config = config.get_prepare_base_model_config()

            prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
            prepare_base_model.get_base_model()
            prepare_base_model.update_base_model()

        except Exception as e:
            raise e


if __name__ == "__main__":
    try:
        logger.info(f"*******************************************")
        logger.info(f">>>>>>>>>>>>>>> stage {STAGE_NAME} <<<<<<<<<<<<<<<")
        obj = PrepareBaseModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
