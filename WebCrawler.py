from main_code.WebCrawler.WebCrawler import WebCrawler
from main_code.Check.CheckBrockImage import CheckBrockImage
from main_code.Repeat.Repeat import Repeat
from pathlib import Path
import threading
import math

# '存圖位置的名稱'、'景點名(組數)' 以及 '圖片編號' 三個數量必須一樣
# '線程數' 不可大於 '8'

# 存圖位置的名稱
name = ['Fenghuang Ancient Town', 'Heavenly Lake, Changbai Mountain',  'Xiaoling Mausoleum of Ming Dynasty']
# 'Bailong Elevator'
# 'Tianmen Mountain'
# 'Zhangjiajie Grand Canyon'
# 'Fenghuang Ancient Town'
# 'Heavenly Lake, Changbai Mountain'
# 'Xiaoling Mausoleum of Ming Dynasty'


# 景點名 多組 * 多個搜尋字
keyword = [
    ['鳳凰古城', 'Fenghuang Ancient Town'],
    ['長白山天池', 'Heavenly Lake, Changbai Mountain'],
    ['明孝陵', 'Xiaoling Mausoleum of Ming Dynasty']
]
# ['百龍天梯', 'Bailong Elevator']
# ['天門山', 'Tianmen Mountain']
# ['張家界大峽谷', 'Zhangjiajie Grand Canyon', '张家界大峡谷']
# ['鳳凰古城', 'Fenghuang Ancient Town']
# ['長白山天池', 'Heavenly Lake, Changbai Mountain']
# ['明孝陵', 'Xiaoling Mausoleum of Ming Dynasty']


# 圖片編號
num = [7250, 5326, 6388]

# 線程數
thread = 2

# ====================分隔線====================

save_path = "./train/"
Path(save_path).mkdir(parents=True, exist_ok=True)

thread_list = []

def crawler(folder_name, keywords, nums):
    print('Crawler Start!')
    WebCrawler(save_path, folder_name, keywords).start(nums)
    print('Crawler End!')

def check(folder_name):
    print('Check Start!')
    CheckBrockImage(save_path, folder_name).start()
    Repeat(save_path, folder_name).start()
    print('Check End!')

if __name__ == '__main__':
    if thread <= 8:
        if len(name) == len(keyword) & len(name) == len(num) & len(keyword) == len(num):
            # 爬圖片
            for i in range(math.ceil(len(name) / thread)):
                for j in range(thread):
                    if (i * thread + j + 1) <= len(name):
                        t = threading.Thread(target=crawler, kwargs={"folder_name": name[i * thread + j], "keywords": keyword[i * thread + j], "nums": num[i * thread + j]})
                        thread_list.append(t)
                
                for t in thread_list:
                    t.setDaemon(True) # 設置守護線程
                    t.start() # 線程啟用

                for t in thread_list:
                    t.join() # 加入線程
                
                thread_list = []

            print('==========Divider==========')
            
            # 檢查圖片
            for i in range(math.ceil(len(name) / thread)):
                for j in range(thread):
                    if (i * thread + j + 1) <= len(name):
                        t = threading.Thread(target=check, kwargs={"folder_name": name[i * thread + j]})
                        thread_list.append(t)
                
                for t in thread_list:
                    t.setDaemon(True) # 設置守護線程
                    t.start() # 線程啟用

                for t in thread_list:
                    t.join() # 加入線程
                
                thread_list = []
            
            print("Complete!")
        elif len(name) != len(keyword) & len(keyword) == len(num):
            print("存圖位置的名稱數量 不一樣!")
        elif len(keyword) != len(name) & len(name) == len(num):
            print('景點名組數 不一樣!')
        elif len(num) != len(name) & len(name) == len(keyword):
            print('圖片編號數量 不一樣!')
    else:
        print('線程數 過大!')
