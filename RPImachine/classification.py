import tensorflow as tf
import cv2
import numpy as np

new_model = tf.keras.models.load_model('my_model.h5')  # 加载已训练模型

def classification(filename, img_height=384, img_width=512):
    class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']


    image = cv2.imread(filename)  # 修改文件名以读取不同图像作为输入
    image_resized = cv2.resize(image, (img_height, img_width))  # 裁剪输入图像以适应模型输入要求
    image = np.expand_dims(image_resized, axis=0)

    pred = new_model.predict(image)

    output_class = class_names[np.argmax(pred)]

    # 展出输入图像及其对应分类
    # plt.figure(figsize=(10, 10))
    # image = cv2.imread(filename)
    # plt.imshow(image)
    # plt.title(output_class)
    # plt.axis('off')
    # plt.show()

    return output_class

def classificationCV2(image, img_height=384, img_width=512):
    class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']


    image_resized = cv2.resize(image, (img_height, img_width))  # 裁剪输入图像以适应模型输入要求
    image = np.expand_dims(image_resized, axis=0)

    pred = new_model.predict(image)

    output_class = class_names[np.argmax(pred)]

    # 展出输入图像及其对应分类
    # plt.figure(figsize=(10, 10))
    # image = cv2.imread(filename)
    # plt.imshow(image)
    # plt.title(output_class)
    # plt.axis('off')
    # plt.show()

    return output_class


# classBelongTo = classification("stabled1.png")
# print(classBelongTo)
# classBelongTo = classification("stabled3.png")
# print(classBelongTo)
# classBelongTo = classification("stabled4.png")
# print(classBelongTo)
# classBelongTo = classification("server.jpg")
# print(classBelongTo)