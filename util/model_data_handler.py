'''
模型数据的获取
'''
import numpy as np

def get_classes(classes_path):
    '''
    获取标签
    :param classes_path:
    :return:装有标签名的 list
    '''
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names


def get_anchors(anchors_path):
    '''
    获取anchor
    :param anchors_path:
    :return: 装有anchor的numpy数组
    '''
    with open(anchors_path) as f:
        anchors = f.readline()
    anchors = [float(x) for x in anchors.split(',')]
    return np.array(anchors).reshape(-1, 2)