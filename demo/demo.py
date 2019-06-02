'''
预测部分
'''
from PIL import Image
import os

def recognize_image(src_image_path):
    for file in os.listdir(src_image_path):
        file_path = os.path.join(src_image_path, file)
        try:
            image = Image.open(file_path)
        except:
            print('Open File Rrror!\n')
            continue
        else:
            # 预测
            # TODO
            return

if __name__ == '__main__':
    recognize_image()
