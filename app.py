import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
from kidneyDiseaseClassifier.pipeline.prediction import PredictionPipeline
from kidneyDiseaseClassifier.utils.common import encode_Image_to_Base64, decodeImage

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
app = Flask(__name__)
CORS(app)


class UserApplication:
    def __init__(self):
        self.filename = "input_img.jpg"
        self.classifier = PredictionPipeline(self.filename)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def prediction():

    if request.method == 'POST':
        # print("REQUEST---> ", request)
        img_base64 = request.json.get('image')

        # print("imge", img_base64)
        # exit()

        decodeImage(img_base64, application.filename)
        result = application.classifier.predict()
        print("result", result)
        return jsonify(result)
    else:
        return jsonify({'error': 'No image data provided'})


if __name__ == "__main__":
    application = UserApplication()
    app.run(host='0.0.0.0', debug=True)
# Compare this snippet from kidneyDiseaseClassifier/pipeline/prediction.py:
