'''
数据增强部分
'''
from PIL import Image
import numpy as np
import os
import xml.etree.ElementTree as ET
import util.node
import util.xml_handler
import math


def rand(a=0, b=1):
    return np.random.rand() * (b - a) + a


def label_rotate(xmin, ymin, xmax, ymax, angle, image_x, image_y):
    '''
    标签标记值的随着图片的转动而改变
    :param xmin: 图片左上角的横坐标
    :param ymin: 图片左上角的纵坐标
    :param xmax: 图片左上角的横坐标
    :param ymax: 图片左上角的纵坐标
    :param angle: 旋转角度
    :param image_x: 图片的宽
    :param image_y: 图片的长
    :return: 旋转后的(xmin,ymin,xmax,ymax) 元组
    '''
    # 角度转换成弧度
    angle = -angle * math.pi / 180.0
    center_x = image_x / 2.0
    center_y = image_y / 2.0
    x = [xmin, xmax, xmin, xmax]
    y = [ymin, ymin, ymax, ymax]
    # 旋转公式
    # x = (x1 - x2)cosθ - (y1 - y2)sinθ + x2
    # y = (x1 - x2)sinθ + (y1 - y2)cosθ + y2
    # 逆时针旋转的情况
    if angle < 0:
        nxmin = (x[0] - center_x) * math.cos(angle) - (y[0] - center_y) * math.sin(angle) + center_x
        nymin = (x[1] - center_x) * math.sin(angle) + (y[1] - center_y) * math.cos(angle) + center_y
        nymax = (x[2] - center_x) * math.sin(angle) + (y[2] - center_y) * math.cos(angle) + center_y
        nxmax = (x[3] - center_x) * math.cos(angle) - (y[3] - center_y) * math.sin(angle) + center_x
    # 顺时针旋转的情况
    else:
        nymin = (x[0] - center_x) * math.sin(angle) + (y[0] - center_y) * math.cos(angle) + center_y
        nxmax = (x[1] - center_x) * math.cos(angle) - (y[1] - center_y) * math.sin(angle) + center_x
        nxmin = (x[2] - center_x) * math.cos(angle) - (y[2] - center_y) * math.sin(angle) + center_x
        nymax = (x[3] - center_x) * math.sin(angle) + (y[3] - center_y) * math.cos(angle) + center_y

    return (str(int(nxmin)), str(int(nymin)), str(int(nxmax)), str(int(nymax)))


def augment(src_image_path, dest_image_path, src_xml_path, dest_xml_path):
    '''
    数据增强部分
    :param src_image_path: 源图片文件
    :param dest_image_path: 源xml文件
    :param src_xml_path: 目标图片文件
    :param dest_xml_path: 目标xml文件
    :return: 无
    '''
    for file in os.listdir(src_image_path):
        file_path = os.path.join(src_image_path, file)
        image = Image.open(file_path)
        tmp = image
        for i in range(20):
            image = tmp
            # 随机生成缩放比例 (针对分辨率)
            # scale = rand(.25, 2)
            # image = image.resize((int(scale * w), int(scale * h)), Image.BICUBIC)
            # 角度范围 [-10,-1] & [1,10]
            scale = i - 10
            # 避免做数字运算的时候除数为 0
            if scale == 0:
                continue
            # 改变图片的旋转程度
            image = image.rotate(scale)
            # 随机调整图片的明暗
            degree = rand(0.8, 1.2)
            image = image.point(lambda p: p * degree)
            image.save(dest_image_path + '\\' + file[0:7] + '_' + str(i + 1) + '.jpg')
            # 对xml文件操作
            my_src_xml_path = os.path.join(src_xml_path, file[0:7] + '.xml')
            my_dest_xml_path = os.path.join(dest_xml_path, file[0:7] + '_' + str(i + 1) + '.xml')

            node_list = []
            in_file = open(my_src_xml_path)
            tree = ET.parse(in_file)
            root = tree.getroot()

            for obj in root.iter('object'):
                cls = obj.find('name').text
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), float(xmlbox.find('xmax').text),
                     float(xmlbox.find('ymax').text))
                # 图片旋转对标记框的标记值也需更改
                nb = label_rotate(b[0], b[1], b[2], b[3], scale, image.size[0], image.size[1])
                one = util.node.Node(cls, '0', nb[0], nb[1], nb[2], nb[3])
                node_list.append(one)
            util.xml_handler.write_xml(node_list, my_dest_xml_path)


if __name__ == "__main__":
    src_image_path = 'JPEGImages'
    dest_image_path = 'generate_image'
    src_xml_path = 'complex_xml'
    dest_xml_path = 'generate_xml'
    augment(src_image_path, dest_image_path, src_xml_path, dest_xml_path)
