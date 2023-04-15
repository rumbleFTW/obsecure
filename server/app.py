import os
import tensorflow as tf
import warnings

warnings.filterwarnings("ignore")

import json
from flask_cors import CORS
from flask import Flask, request

import numpy as np
from PIL import Image
import requests

from io import BytesIO

os.environ["CUDA_VISIBLE_DEVICES"] = ""

app = Flask(__name__)
cors = CORS(app)

global MODEL
global CLASSES


@app.route("/", methods=["GET"])
def default():
    return json.dumps({"Hello I am Chitti": "Speed 1 Terra Hertz, Memory 1 Zeta Byte"})


@app.route("/predict", methods=["GET"])
def predict():
    src = request.args.get("src")
    response = requests.get(src)
    try:
        image = Image.open(BytesIO(response.content))
        image = image.resize((128, 128))
        image = np.array(image)
        image = image.astype("float") / 255.0
        image = np.expand_dims(image, axis=0)
        pred = MODEL.predict(image)
        return json.dumps({"class": CLASSES[int(np.argmax(pred, axis=1))]})
    except:
        return json.dumps({"Uh oh": "We are down"})


if __name__ == "__main__":
    MODEL_PATH = os.path.abspath("./models/image/dump/mobile_net.h5")
    MODEL = tf.keras.models.load_model(MODEL_PATH)
    CLASSES = ["control", "gore", "pornography"]
    app.run(threaded=True, debug=True)
