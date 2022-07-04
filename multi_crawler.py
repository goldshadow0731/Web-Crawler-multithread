from math import ceil
import os
from threading import Thread, Lock

from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, GoogleFeeder

from module.check_image import CheckImage
from module.check_repeat import CheckRepeat


# category_name: ['category_keyword_1', 'category_keyword_2', ...]
categories = {
    'Car': ['car', 'bus', 'SUV'],
    'Train': ['train']
}

max_num = 1000

# ==================== Split ====================


# Crawler
for category, keywords in categories.items():
    for image_crawler in [GoogleImageCrawler, BingImageCrawler]:
        for keyword in keywords:
            crawler = image_crawler(feeder_threads=1,
                                    parser_threads=1,
                                    downloader_threads=4,
                                    storage={'root_dir': f'./images/{category}'})
            crawler.crawl(keyword=keyword, max_num=max_num)


# Check
def check(category_name, save_path, lock):
    complete, incomplete, error = CheckImage.run(
        os.path.join(save_path, category_name))
    lock.acquire()
    print(f'\nCheck Image - {category_name}')
    print(f'{category_name:<10s} - {"normal":>8s}: {complete:5d}')
    print(f'{category_name:<10s} - {"distory":>8s}: {incomplete:5d}')
    print(f'{category_name:<10s} - {"error":>8s}: {error:5d}')
    lock.release()

    images, delete = CheckRepeat.run(os.path.join(save_path, category_name))
    lock.acquire()
    print(f'\nCheck Repect - {category_name}')
    print(f'{category_name:<10s} - {"remain":>8s}: {images:5d}')
    print(f'{category_name:<10s} - {"delete":>8s}: {delete:5d}')
    lock.release()


steps = ceil(len(categories.keys()) / os.cpu_count())
save_path = "./images"
lock = Lock()

for i in range(steps):
    thread_list = list()
    for j in range(len(categories.keys()) if len(categories.keys()) < os.cpu_count() else os.cpu_count()):
        count = i * os.cpu_count() + j
        if count < len(categories.keys()):
            thread_list.append(
                Thread(target=check, kwargs={
                    "category_name": list(categories.keys())[count],
                    "save_path": save_path,
                    "lock": lock}
                )
            )

    for t in thread_list:
        # t.setDaemon(True)  # Set Daemon thread
        t.start()  # Thread enable

    for t in thread_list:
        t.join()  # Join thread
