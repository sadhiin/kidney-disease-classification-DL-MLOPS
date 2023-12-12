from kidneyDiseaseClassifier.config.configuration import PretrainModelConfigurationManager
from kidneyDiseaseClassifier.components.model_evaluation import Evaluation
from kidneyDiseaseClassifier import logger

SAGE_NAME = "Evaluation Stage"


class EvaluationPipeline:
    def __init__(self):
        pass

    def run(self):
        config = PretrainModelConfigurationManager(model_name="VGG16")
        evaluation_config = config.get_evaluation_config()
        model_evaluation = Evaluation(config=evaluation_config)

        model_evaluation.evaluation()
        model_evaluation.save_score()
        model_evaluation.log_into_mlflow()


if __name__ == "__main__":
    try:
        logger.info(f"###################################################")
        logger.info(f">>>>>>>>>>>>>>>>>>> Starting stage {SAGE_NAME} <<<<<<<<<<<<<<<<<<<<")
        obj = EvaluationPipeline()
        obj.run()
        logger.info(f">>>>>>>>>>>>>>>>>>> Finished stage {SAGE_NAME} <<<<<<<<<<<<<<<<<<<<")
    except Exception as e:
        raise e
