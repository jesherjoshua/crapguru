#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify
import requests
import tensorflow as tf
import numpy as np
import json
import os

app = Flask(__name__)

UPLOADS = './static/uploads/'

def pre_process(img):
    img = tf.keras.preprocessing.image.load_img(img, target_size=(96, 96))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img


@app.route('/',methods=['GET','POST'])
def home():
    return render_template("home.html")


@app.route("/resultpage", methods=["POST", "GET"])
def result():
    if(request.method=="POST"):
        img = request.files['filename']
        img.save(UPLOADS+'test.jpg')
        img = pre_process(UPLOADS+'test.jpg')
        url='https://thecrapfunction-vfof3shfeq-uc.a.run.app'
        payload = json.dumps({"instances": img.tolist()})
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, data=payload, headers=headers)
        result = response.json()
        pred = result["predictions"]
        if pred == 0:
            txt ="Your Waste is Bio-Degradable! 🌏"
        else:
            txt ="Your Waste is Treatable ♻️, Separate from other wet waste!"
        print(txt)
        os.remove(UPLOADS+'test.jpg')
        return jsonify({"pred":pred,"text":txt})


@app.route('/info')
def info():
    return render_template("info.html")


if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0",port="8080")