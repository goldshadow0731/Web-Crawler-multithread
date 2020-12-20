#批量修改尺寸
import os
from PIL import Image
from pathlib import Path

dir_floders="./train/"
dir_save="./result/"

Path(dir_save).mkdir(parents=True, exist_ok=True)

size=(400,400)

#获取目录下所有图片名
for dir_img in os.listdir(dir_floders):
    print(dir_img)
    list_temp = os.listdir(dir_floders + dir_img + '/')
    list_img = list_temp[0:]

    #获得路径、打开要修改的图片
    for img_name in list_img:
        if img_name == 'Thumbs.db':
            continue
        print(img_name)
        img_path = dir_floders + dir_img + '/' + img_name
        old_image = Image.open(img_path)
        save_path = dir_save + dir_img + '/' + img_name

        Path((dir_save + dir_img + '/')).mkdir(parents=True, exist_ok=True)

        #保存修改尺寸后的图片
        old_image.resize(size, Image.ANTIALIAS).save(save_path)
print("Done!")
