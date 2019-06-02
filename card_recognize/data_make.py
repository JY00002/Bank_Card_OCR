'''
制作数据集

先将所有数据分成训练集、测试集、验证集，再将每个集合的所有xml中所有box
的顶点坐标以及类型存在一个txt文件中
'''

import os
import random
import xml.etree.ElementTree as ET

# sets：数据所属的集合名称
sets = ['train', 'test']

root_path = os.path.abspath(os.path.join(os.getcwd(), ".."))

def get_classes():
    class_file = open("model_data/classes.txt", "r")
    classes = class_file.read().splitlines()
    class_file.close()
    return classes

def data_split():
    '''
    将数据集，即xml文件分成训练集、测试集和交叉验证集

    先将总数据分成按照8:2的比例分成训练集和训练验证集，再将
    训练验证集按照8:2的比例分成测试集和交叉验证集，将数据的
    文件名存储在dataset/name目录下。训练集、测试集、交叉验
    证集分别存放在train.txt、test.txt、val.txt中。
    '''
    train_val_percent = 0.2
    test_percent = 0.8
    xml_filepath = '../dataset/annotation'
    total_xml = os.listdir(xml_filepath)

    num = len(total_xml)
    list = range(num)

    train_num = int(num * test_percent)

    train = random.sample(list, train_num)

    test_file = open('../dataset/name/test.txt', 'w')
    train_file = open('../dataset/name/train.txt', 'w')

    for file in list:
        name = total_xml[file][:-4] + '\n'
        if file not in train:
            test_file.write(name)
        else:
            train_file.write(name)

    train_file.close()
    test_file.close()


def convert_annotation(image_id, list_file):
    '''
    将xml文件每个box的顶点（左上、右下）的坐标以及类型取出来，依次存入文件中

    (xmin, ymin)代表box左上角的坐标，(xmax, ymax)代表box右下角的坐标，cls_id代表box的类型
    将上述数据依次写入文件list_file中，并用逗号分隔
    :param image_id: 图片的名字
    :param list_file: 数据集类型（训练集、测试集、验证集）
    '''
    in_file = open('../dataset/annotation/%s.xml' % image_id)
    tree = ET.parse(in_file)
    root = tree.getroot()
    classes = get_classes()

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xml_box = obj.find('bndbox')
        # cor_list是所有box坐标的集合
        cor_list = (int(xml_box.find('xmin').text), int(xml_box.find('ymin').text),
                    int(xml_box.find('xmax').text), int(xml_box.find('ymax').text))
        list_file.write(" " + ",".join([str(cor) for cor in cor_list]) + ',' + str(cls_id))


def add_path():
    '''
    添加文件路径并保存

    将图片路径添加在数据前面，并将文件保存至dataset/label中
    '''
    for image_set in sets:
        image_ids = open('../dataset/name/%s.txt' % image_set).read().strip().split()
        list_file = open('../dataset/label/%s_label.txt' % image_set, 'w')
        for image_id in image_ids:
            list_file.write('%s/dataset/images/%s.jpg' % (root_path, image_id))
            convert_annotation(image_id, list_file)
            list_file.write('\n')
        list_file.close()


if __name__ == '__main__':
    data_split()
    add_path()
