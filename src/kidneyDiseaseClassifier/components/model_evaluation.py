import tensorflow as tf
from pathlib import Path
import mlflow
import mlflow.keras
from urllib.parse import urlparse
from kidneyDiseaseClassifier.utils.common import save_json
from kidneyDiseaseClassifier.entity.config_entity import EvaluationConfig


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config
        self.model = None
        self.score = None

    def _valid_generator(self):

        data_generator_kwargs = dict(
            rescale=1. / 255,
            validation_split=0.3
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size
        )

        valid_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(**data_generator_kwargs)

        self.valid_generator = valid_data_generator.flow_from_directory(
            directory=self.config.training_data,
            subset='validation',
            seed=324893,
            shuffle=False,
            **dataflow_kwargs
        )

    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)

    def save_score(self):
        scores = {'loss': self.score[0], 'accuracy': self.score[1]}
        save_json(path=Path('score.json'), data=scores)

    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        print(self.valid_generator.class_names)
        self.score = self.model.evaluate(self.valid_generator)
        self.save_score()

    def log_into_mlflow(self):
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            print(self.config.all_params)
            mlflow.log_params(self.config.all_params)
            mlflow.log_metrics({'loss': self.score[0], 'accuracy': self.score[1]})

            # model registry
            if tracking_url_type_store != 'file':
                # register the model
                # There are other ways to use the model registry, which depends on the user case,
                # please refer to the doc for more information:
                # at https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.keras.log_model(self.model, 'model', registered_model_name='VGG16')
            else:
                mlflow.keras.log_model(self.model, "model")
