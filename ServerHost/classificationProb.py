import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt

new_model = tf.keras.models.load_model('my_model1.h5')

def classification(filename, img_height=224, img_width=224):
    class_names = ['glass', 'plastic', 'recycle', 'trash']
    image = cv2.imread(filename)  # 修改文件名以读取不同图像作为输入
    image_resized = cv2.resize(image, (img_height, img_width))  # 裁剪输入图像以适应模型输入要求
    image = np.expand_dims(image_resized, axis=0)

    pred = new_model.predict(image)
    for result in pred:
        continue

    probability = []

    for i in result:
        if i < 0.00001:
            x = 0
        else:
            x = str(round(float(i) * 100, 2))
        probability.append(x)

    output_class = class_names[np.argmax(pred)]

    # 展出输入图像及其对应分类
    plt.figure(figsize=(10, 10))
    image = cv2.imread(filename)
    plt.imshow(image)
    plt.title(output_class, fontsize=30, font='Arial')
    for s in range(4):
        y = 7*(s+1)
        words = class_names[s] + ': ' + str(probability[s]) + '%'
        plt.text(1, y, words, color='w')
    plt.axis('off')
    plt.show()

    return output_class


classBelongTo = classification("8.jpg")
print(classBelongTo)
