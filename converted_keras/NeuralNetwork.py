import pandas as pd
from tensorflow.python.keras.models import load_model
from PIL import Image, ImageOps
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import *
import cv2
import os
pd.options.display.notebook_repr_html=False  # 表格显示
plt.rcParams['figure.dpi'] = 75  # 图形分辨率
sns.set_theme(style='darkgrid')  # 图形主题


# Load the model
model = load_model('keras_model.h5')
path = "./../archive/test-set/"
test_size = len(os.listdir(path))
test_data = np.ndarray(shape=(test_size, 224, 224, 3), dtype=np.float32)
test_pokemon_name = []
re_han = re.compile("[0-9]*?px.*?([A-Za-z-]*?).jpg")

count = 0
for image_name in os.listdir(path):     # 获取每个测试图片
    image_path = os.path.join(path, image_name)
    image_ = Image.open(image_path)
    image_ = image_.convert('RGB')
    size = (224, 224)
    image_ = ImageOps.fit(image_, size, Image.ANTIALIAS)
    image_array = array(image_)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    pokemon_name = re.match(re_han, image_name).group(1)
    test_pokemon_name.append(pokemon_name)
    # print(test_data.shape())
    test_data[count] = normalized_image_array
    count += 1

prediction = model.predict(test_data)

classify_dict = {}
with open("./labels.txt", "r") as r:
    lines = r.readlines()

for line in lines:
    classify_dict[int(line[0])] = line[2:].strip()

for idx in range(len(prediction)):
    print(f"{test_pokemon_name[idx]}'s type prediction is")
    i = 0
    df = pd.DataFrame({"Type": list(classify_dict.values()), "Prediction": prediction[idx]})
    sns.barplot(data=df, x="Type", y='Prediction')
    plt.show()
    break
    for p in prediction[idx]:
        print('{}:{:.2%}'.format(classify_dict[i], p))
        i += 1
