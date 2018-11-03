# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import pprint

# use pil package to open the image and convert the image to gray one
im = Image.open('img/cat.jpg').convert('L').save('img/cat_new.png')
print('write the image to gray one, ok.')

# 使用matplotlib读取图像然后保存为numpy中的数组
color_img = np.array(plt.imread('img/cat.jpg'))
shape = color_img.shape

# 循环遍历数组进行RGB图像的灰度合成
gray_image = np.zeros((shape[0], shape[1]))
for i in range(shape[0]):
    for j in range(shape[1]):
        gray_image[i, j] = color_img[i, j, 0] * 0.299 + color_img[i,  j,  0] * 0.587 + color_img[i, j, 0] * 0.114

# 使用matplotlib写入图像
plt.imsave('img/gray_new_2.png', gray_image)

# 查看matplotlib支持的数据格式
pprint.pprint(plt.gcf().canvas.get_supported_filetypes())
