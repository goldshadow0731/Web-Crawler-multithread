from selenium import webdriver
import time
import urllib.request
import os
from pathlib import Path

#百度
#url = 'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word='+S
#xpath = '//div[@id="imgid"]/div/ul/li/div/a/img'

#搜狗
#url = 'https://pic.sogou.com/pics?query=' + S + '&di=2&_asf=pic.sogou.com&w=05009900'
#xpath = '//div[@class="figure-result"]/ul/li/div/a/img'

#360
#url = 'https://image.so.com/i?q='+ S +'&src=tab_www'
#xpath = '//div[@class="stream"]/div/div/div/ul/li/div/a/span/img'

#bing
#url = 'https://www.bing.com/images/search?q=' + S + '&form=HDRSC2&first=1&scenario=ImageBasicHover&cw=1117&ch=864'
#xpath = '//div[@id="b_content"]/div[@id="vm_c"]/div[@class="dg_b"]/div/ul/li/div/div/a/div[@class="img_cont hoff"]/img'

#google
#url = 'https://www.google.com.tw/search?q='+S+'&tbm=isch&ved=2ahUKEwiwvsi-y5_tAhVH4GEKHe5JBUwQ2-cCegQIABAA&oq=%E8%B2%93&gs_lcp=CgNpbWcQAzIECCMQJzIECCMQJzIFCAAQsQMyBQgAELEDMgUIABCxAzIFCAAQsQMyAggAMgUIABCxAzICCAAyBQgAELEDOgcIIxDqAhAnUN0WWJseYPkhaAFwAHgBgAG3AYgBugWSAQMwLjWYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCsABAQ&sclient=img&ei=KEy_X7CKE8fAhwPuk5XgBA&authuser=0&bih=687&biw=1455&hl=zh-TW'
#xpath = '//div[@id="islrg"]/div/div/a[@class="wXeWr islib nfEiy mM5pbd"]/div[@class="bRMDJf islir"]/img'

#等一下要爬的url
url_head = [
    'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=',
    'https://pic.sogou.com/pics?query=',
    'https://image.so.com/i?q=',
    'https://www.bing.com/images/search?q=',
    'https://www.google.com.tw/search?q='
]

url_end = [
    '',
    '&di=2&_asf=pic.sogou.com&w=05009900',
    '&src=tab_www',
    '&form=HDRSC2&first=1&scenario=ImageBasicHover&cw=1117&ch=864',
    '&tbm=isch&ved=2ahUKEwiwvsi-y5_tAhVH4GEKHe5JBUwQ2-cCegQIABAA&oq=%E8%B2%93&gs_lcp=CgNpbWcQAzIECCMQJzIECCMQJzIFCAAQsQMyBQgAELEDMgUIABCxAzIFCAAQsQMyAggAMgUIABCxAzICCAAyBQgAELEDOgcIIxDqAhAnUN0WWJseYPkhaAFwAHgBgAG3AYgBugWSAQMwLjWYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCsABAQ&sclient=img&ei=KEy_X7CKE8fAhwPuk5XgBA&authuser=0&bih=687&biw=1455&hl=zh-TW'
]

url_xpath = [
    '//div[@id="imgid"]/div/ul/li/div/a/img',
    '//div[@class="figure-result"]/ul/li/div/a/img',
    '//div[@class="stream"]/div/div/div/ul/li/div/a/span/img',
    '//div[@id="b_content"]/div[@id="vm_c"]/div[@class="dg_b"]/div/ul/li/div/div/a/div[@class="img_cont hoff"]/img',
    '//div[@id="islrg"]/div/div/a[@class="wXeWr islib nfEiy mM5pbd"]/div[@class="bRMDJf islir"]/img'
]

class WebCrawler:
    def __init__(self, save_path, save_folder_name, keywords):
        self.first_path = save_path
        self.save_folder_name = save_folder_name
        self.keywords = keywords

    def imagesCrawler(self, nums):
        # chromedriver檔案放的位置
        chrome_driver = './chromedriver/chromedriver'

        # 實際存圖位置
        local_path = self.first_path + self.save_folder_name

        #如果沒有資料夾會自動建立一個
        Path(local_path).mkdir(parents=True, exist_ok=True)
        
        for i in range(len(self.keywords)):
            keyword = self.keywords[i]
            
            # 爬取頁面網址 目標元素的xpath
            for j in range(5):
                print(self.save_folder_name,"-搜尋引擎：",j)
                url = url_head[j] + keyword + url_end[j]
                xpath = url_xpath[j]

                # 啟動chrome瀏覽器
                driver = webdriver.Chrome(chrome_driver)

                # 最大化窗口，因為每一次爬取只能看到視窗内的圖片
                driver.maximize_window()

                # 紀錄下載過的圖片網址，避免重複下載
                img_url_dic = {}

                # 瀏覽器打開爬取頁面
                driver.get(url)

                # 模擬滾動視窗瀏覽更多圖片
                pos = 0
                for k in range(100):
                    print(self.save_folder_name,"-下滾：",k)
                    pos += k * 500  # 每次下滾500
                    js = "document.documentElement.scrollTop=%d" % pos
                    driver.execute_script(js)
                    time.sleep(0.01)

                    for element in driver.find_elements_by_xpath(xpath):
                        try:
                            img_url = element.get_attribute('src')

                            # 保存圖片到指定路徑
                            if img_url != None and not img_url in img_url_dic:
                                img_url_dic[img_url] = ''
                                filename = str(nums) + '_' + keyword + '.jpg'
                                nums += 1
                                print(self.save_folder_name,"-檔案名稱：",filename)

                                # 保存圖片
                                urllib.request.urlretrieve(img_url, os.path.join(local_path, filename))

                        except OSError:
                            print(self.save_folder_name,'-發生OSError!')
                            print(self.save_folder_name,'-',pos)
                            break

                driver.close()

    def start(self, nums):
        self.imagesCrawler(nums)

