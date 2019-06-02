"""Miscellaneous utility functions."""

from functools import reduce

import numpy as np
from PIL import Image
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb


def compose(*funcs):
    """Compose arbitrarily many functions, evaluated left to right.

    Reference: https://mathieularose.com/function-composition-in-python/
    """
    # return lambda x: reduce(lambda v, f: f(v), funcs, x)
    if funcs:
        return reduce(lambda f, g: lambda *a, **kw: g(f(*a, **kw)), funcs)
    else:
        raise ValueError('Composition of empty sequence not supported.')


# def letterbox_image(image, size):
#     '''resize image with unchanged aspect ratio using padding'''
#     iw, ih = image.size
#     w, h = size
#     scale = min(w / iw, h / ih)
#     nw = int(iw * scale)
#     nh = int(ih * scale)
#
#     image = image.resize((nw, nh), Image.BICUBIC)
#     new_image = Image.new('RGB', size, (128, 128, 128))
#     new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
#     return new_image


def rand(a=0, b=1):
    return np.random.rand() * (b - a) + a


def get_random_data(annotation_line, input_shape, random=True, max_boxes=20, jitter=.3, hue=.1, sat=1.5, val=1.5,
                    proc_img=True):
    '''random preprocessing for real-time data augmentation'''
    line = annotation_line.split()
    image = Image.open(line[0])
    iw, ih = image.size
    print(iw, ih)
    h, w = input_shape
    box = np.array([np.array(list(map(int, box.split(',')))) for box in line[1:]])
    if random:
        # 缩放大小
        scale = min(w / iw, h / ih)
        nw = int(iw * scale)
        nh = int(ih * scale)
        print(nw, nh)
        print("------------------------")
        # 中心点
        dx = (w - nw) // 2
        dy = (h - nh) // 2
        image_data = 0
        if proc_img:
            image = image.resize((nw, nh), Image.BICUBIC)
            # 背景
            new_image = Image.new('RGB', (w, h), (128, 128, 128))
            # 黏贴图
            new_image.paste(image, (dx, dy))
            # 归一化
            image_data = np.array(new_image) / 255.

        # 定义新的BOX位置
        box_data = np.zeros((max_boxes, 5))
        if len(box) > 0:
            np.random.shuffle(box)
            # 最大 20 个 BOX
            if len(box) > max_boxes: box = box[:max_boxes]
            # 根据缩放大小，生成新图中的 BOX 位置
            box[:, [0, 2]] = box[:, [0, 2]] * scale + dx
            box[:, [1, 3]] = box[:, [1, 3]] * scale + dy
            box_data[:len(box)] = box

        return image_data, box_data

    #  随机生成宽高比
    new_ar = w / h * rand(1 - jitter, 1 + jitter) / rand(1 - jitter, 1 + jitter)
    # 随机生成缩放比例
    scale = rand(.25, 2)
    # 生成新的高宽数据，可能放大2倍
    if new_ar < 1:
        nh = int(scale * h)
        nw = int(nh * new_ar)
    else:
        nw = int(scale * w)
        nh = int(nw / new_ar)
    image = image.resize((nw, nh), Image.BICUBIC)

    # 随机水平位移
    dx = int(rand(0, w - nw))
    dy = int(rand(0, h - nh))
    new_image = Image.new('RGB', (w, h), (128, 128, 128))
    new_image.paste(image, (dx, dy))
    image = new_image

    # 翻转
    flip = rand() < .5
    if flip: image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # 颜色抖动 HSV抖动
    hue = rand(-hue, hue)
    sat = rand(1, sat) if rand() < .5 else 1 / rand(1, sat)
    val = rand(1, val) if rand() < .5 else 1 / rand(1, val)
    # 归一化处理
    # 内部函数，通过公式转化
    x = rgb_to_hsv(np.array(image) / 255.)
    x[..., 0] += hue
    x[..., 0][x[..., 0] > 1] -= 1
    x[..., 0][x[..., 0] < 0] += 1
    x[..., 1] *= sat
    x[..., 2] *= val
    # 避免S/V CHANNEL越界
    x[x > 1] = 1
    x[x < 0] = 0
    image_data = hsv_to_rgb(x)  # numpy array, 0 to 1

    # 定义新的BOX位置
    # YOLO是位置检测的算法，在经过缩放和水平变换后，BOX的左边也需要相应的变化
    box_data = np.zeros((max_boxes, 5))
    if len(box) > 0:
        np.random.shuffle(box)
        box[:, [0, 2]] = box[:, [0, 2]] * nw / iw + dx
        box[:, [1, 3]] = box[:, [1, 3]] * nh / ih + dy
        # 左右翻转
        if flip: box[:, [0, 2]] = w - box[:, [2, 0]]
        # 定义边界
        box[:, 0:2][box[:, 0:2] < 0] = 0
        box[:, 2][box[:, 2] > w] = w
        box[:, 3][box[:, 3] > h] = h
        # 计算新的长宽
        box_w = box[:, 2] - box[:, 0]
        box_h = box[:, 3] - box[:, 1]
        box = box[np.logical_and(box_w > 1, box_h > 1)]  # discard invalid box
        if len(box) > max_boxes: box = box[:max_boxes]
        box_data[:len(box)] = box

    return image_data, box_data
