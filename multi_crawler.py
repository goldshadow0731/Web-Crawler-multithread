from math import ceil
import os
from threading import Thread

from module.web_crawler import WebCrawler
from module.check_image import CheckImage
from module.check_repeat import CheckRepeat


# category_name: ['category_keyword_1', 'category_keyword_2', ...]
category = {
    'Train': ['train', 'railway'],
    'BUS': ['bus']
}

# image start label, need to match category | default: 0
num = []

# max image | Upper limit. None = no limit
max_count = 10

# image label format
format_type = "{num:04d}_{keyword}.jpg"

# Used thread | less than 9
use_thread = 2

# Save path
save_path = "./images"

# ==================== Split ====================
os.makedirs(save_path, exist_ok=True)


def crawler(category_name, save_path, format_type, keywords, num, max_count):
    print('Crawler Start!')
    WebCrawler(category_name, save_path, format_type).run(
        keywords, num, max_count)
    print('Crawler End!')


def check(category_name, save_path):
    print('Check Start!')
    complete, incomplete, error = CheckImage.run(
        os.path.join(save_path, category_name))
    print(f'Check Image - {category_name}')
    print(f'{category} - {"normal":>8s}: {complete:5d}')
    print(f'{category} - {"distory":>8s}: {incomplete:5d}')
    print(f'{category} - {"error":>8s}: {error:5d}')
    print("\n")
    images, delete = CheckRepeat.run(os.path.join(save_path, category_name))
    print(f'Check Repect - {category_name}')
    print(f'{category} - {"remain":>8s}: {images:5d}')
    print(f'{category} - {"delete":>8s}: {delete:5d}')
    print("\n")
    print('Check End!')


if __name__ == '__main__':
    if use_thread > 8:
        print('Thread is bigger than 8!')
    else:
        # Crawler image
        for i in range(ceil(len(category.keys()) / use_thread)):
            thread_list = list()

            for j in range(use_thread):
                count = i * use_thread + j
                if count < len(category.keys()):
                    thread_list.append(
                        Thread(target=crawler, kwargs={
                            "category_name": list(category.keys())[count],
                            "save_path": save_path,
                            "format_type": format_type,
                            "keywords": list(category.values())[count],
                            "num": num[count] if count < len(num) else 0,
                            "max_count": max_count}
                        )
                    )

            for t in thread_list:
                # t.setDaemon(True)  # Set Daemon thread
                t.start()  # Thread enable

            for t in thread_list:
                t.join()  # Join thread

        print('========== Split ==========')

        # Check image
        for i in range(ceil(len(category.keys()) / use_thread)):
            thread_list = list()
            for j in range(use_thread):
                count = i * use_thread + j
                if count < len(category.keys()):
                    thread_list.append(
                        Thread(target=check, kwargs={
                            "category_name": list(category.keys())[count],
                            "save_path": save_path}
                        )
                    )

            for t in thread_list:
                # t.setDaemon(True)  # Set Daemon thread
                t.start()  # Thread enable

            for t in thread_list:
                t.join()  # Join thread

        print("Complete!")
