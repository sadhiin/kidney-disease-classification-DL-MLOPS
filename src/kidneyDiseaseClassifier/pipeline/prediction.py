import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


class PredictionPipeline:

    def __init__(self, filename) -> None:
        self.filename = filename

    def predict(self):
        # load model
        model = load_model(os.path.join("artifacts", "training", "trained_model.keras"))
        image_name = self.filename
        test_image = image.load_img(image_name, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)
        result = np.argmax(result, axis=1)
        prediction = None
        if result == 0:
            prediction = 'Cyst'
        elif result == 1:
            prediction = 'Tumer'
        elif result == 2:
            prediction = 'Stone'
        elif result == 3:
            prediction = 'Normarl'

        return [{"image": prediction}]