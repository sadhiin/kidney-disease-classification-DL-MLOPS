import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from pathlib import Path
from kidneyDiseaseClassifier.entity.config_entity import PrepareBaseModelConfig


class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.model = None
        self.config = config

    def get_base_model(self):
        self.model = tf.keras.applications.vgg16.VGG16(
            input_shape=self.config.params_image_size,
            weights=self.config.params_weights,
            include_top=self.config.params_include_top
        )

        self.save_model(path=self.config.base_model_path, model=self.model)

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate, dropout_rate):
        # Freeze the pretrained weights
        if freeze_all:
            for layer in model.layers:
                layer.trainable = False

            no_of_layers = len(model.layers)
            no_of_layers_to_train = int(no_of_layers / 2)

            # Skipping the BN layers
            for layer in model.layers[-no_of_layers_to_train:]:
                if not isinstance(layer, tf.keras.layers.BatchNormalization):
                    layer.trainable = True

        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model[:freeze_till]:
                if not isinstance(layer, tf.keras.layers.BatchNormalization):
                    layer.trainable = True
                else:
                    layer.trainable = False

        # Rebuild top
        x = tf.keras.layers.GlobalAveragePooling2D(name="avg_pool")(model.output)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(dropout_rate, name="top_dropout")(x)
        x = tf.keras.layers.Dense(256)(x)
        x = tf.keras.layers.Dense(128)(x)
        
        prediction = tf.keras.layers.Dense(
            units=classes,
            activation='softmax',
            name="pred"
        )(x)

        full_model = tf.keras.models.Model(
            inputs=model.input,
            outputs=prediction
        )

        full_model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.9),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=['accuracy']
        )

        full_model.summary()
        return full_model

    def update_base_model(self):
        self.full_model = self._prepare_full_model(
            model=self.model,
            classes=self.config.params_classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config.params_learning_rate,
            dropout_rate=self.config.params_dropout_rate
        )

        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)

