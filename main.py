from flask import Flask
from flask import request
import os
import io
import base64
from PIL import Image

# from yolo import YOLO, detect_video
# import yolo_video

# import YOLO as yolo

app = Flask(__name__)


#
# #index
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     fileSrc = "./ceshi/1.jpg"
#     img2 = Image.open(fileSrc)
#     yolo_video.detect_img2(img2, fileSrc)
#     return "home"

# @app.route('/prediction', methods=['GET', 'POST'])
# def prediction():
#     img_data_base64 = request.form['data']
#     # print(img_data_base64)
#     img_data=base64.b64decode(img_data_base64)
#     image=io.BytesIO(img_data)
#
#     img = Image.open(image)
#     fileSrc = "./ceshi/1.jpg"
#     # img.show()
#     img.save(fileSrc)
#
#     predNum = yolo_video.detect_img2(img, fileSrc)
#
#     print(predNum)
#     return str(predNum)

@app.route('/index', methods=['GET', 'POST'])
def index():
    return 'index'


if __name__ == '__main__':
    # yolo = YOLO()
    app.run(host='0.0.0.0', port=5001)
