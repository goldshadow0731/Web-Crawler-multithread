import os
from PIL import Image

image_path = "./images"
resize_path = "./resize"

target_size = (400, 400)

os.makedirs(resize_path, exist_ok=True)

for sub_path in os.listdir(image_path):
    category_path = os.path.join(image_path, sub_path)
    os.makedirs(os.path.join(resize_path, sub_path), exist_ok=True)
    print(sub_path)

    for img_name in os.listdir(category_path):
        if os.path.isfile(img_name):
            print(img_name)
            old_image = Image.open(os.path.join(category_path, img_name))
            save_path = os.path.join(resize_path, sub_path, img_name)
            old_image.resize(target_size, Image.ANTIALIAS).save(save_path)

print("Done!")
