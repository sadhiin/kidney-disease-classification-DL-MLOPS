from kidneyDiseaseClassifier import logger
from kidneyDiseaseClassifier.config.configuration import PrepareBaseModelConfig
from kidneyDiseaseClassifier.components.model_training import Training

STAGE_NAME = "Training"
class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = PrepareBaseModelConfig(model_name="VGG16")
        training_config = config.get_training_config()

        trainer = Training(config=training_config)

        trainer.get_base_model()
        trainer.train_valid_generator()
        trainer.train(callbacks_list=None)


if __name__ == "__main__":
    try:
        logger.info("#####################################")
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<<<<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<\n\nx========================x\n\n")
    except Exception as e:
        logger.exception(e)
        raise e
