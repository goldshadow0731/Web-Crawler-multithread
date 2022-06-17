import os
import time
from urllib.request import urlretrieve

from selenium import webdriver


class WebCrawler:
    chrome_driver = './chromedriver/chromedriver'
    search_engine = {
        "baidu": {
            "url": "http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word={keyword}",
            "xpath": '//div[@id="imgid"]/div/ul/li/div/a/img'
        },
        "sogou": {
            "url": "https://pic.sogou.com/pics?query={keyword}&di=2&_asf=pic.sogou.com&w=05009900",
            "xpath": '//div[@class="figure-result"]/ul/li/div/a/img'
        },
        "360": {
            "url": "https://image.so.com/i?q={keyword}&src=tab_www",
            "xpath": '//div[@class="stream"]/div/div/div/ul/li/div/a/span/img'
        },
        "bing": {
            "url": "https://www.bing.com/images/search?q={keyword}&form=HDRSC2&first=1&scenario=ImageBasicHover&cw=1117&ch=864",
            "xpath": '//div[@id="b_content"]/div[@id="vm_c"]/div[@class="dg_b"]/div/ul/li/div/div/a/div[@class="img_cont hoff"]/img'
        },
        "google": {
            "url": "https://www.google.com.tw/search?q={keyword}&tbm=isch&ved=2ahUKEwiwvsi-y5_tAhVH4GEKHe5JBUwQ2-cCegQIABAA&oq=%E8%B2%93&gs_lcp=CgNpbWcQAzIECCMQJzIECCMQJzIFCAAQsQMyBQgAELEDMgUIABCxAzIFCAAQsQMyAggAMgUIABCxAzICCAAyBQgAELEDOgcIIxDqAhAnUN0WWJseYPkhaAFwAHgBgAG3AYgBugWSAQMwLjWYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCsABAQ&sclient=img&ei=KEy_X7CKE8fAhwPuk5XgBA&authuser=0&bih=687&biw=1455&hl=zh-TW",
            "xpath": '//div[@id="islrg"]/div/div/a[@class="wXeWr islib nfEiy mM5pbd"]/div[@class="bRMDJf islir"]/img'
        }
    }

    def __init__(self, category_name, save_path='./images', format_type="{num:04d}_{keyword}.jpg"):
        self.category_path = os.path.join(save_path, category_name)
        os.makedirs(self.category_path, exist_ok=True)
        self.category_name = category_name
        self.format_type = format_type

    def run(self, keywords, num=0, max_count=None):
        start_num = num
        reach_limit = False
        for keyword in keywords:
            downloaded_img_url = []

            for search_engine_name, search_engine_info in self.search_engine.items():
                print(f"{self.category_name} - Search engine: {search_engine_name}")

                driver = webdriver.Chrome(self.chrome_driver)
                driver.maximize_window()
                driver.get(search_engine_info["url"].format(keyword=keyword))

                pos = 0  # roll down
                for k in range(100):
                    # print(f"{self.category_name} - Roll: {k}")
                    pos += k * 500
                    js = f"document.documentElement.scrollTop={pos}"
                    driver.execute_script(js)
                    time.sleep(0.01)

                    for element in driver.find_elements_by_xpath(search_engine_info["xpath"]):
                        try:
                            img_url = element.get_attribute('src')

                            if img_url != None and not img_url in downloaded_img_url:
                                downloaded_img_url.append(img_url)
                                filename = self.format_type.format(
                                    num=num, keyword=keyword)
                                num += 1

                                print(
                                    f"{self.category_name} - Filename： {filename}")
                                urlretrieve(
                                    img_url, os.path.join(self.category_path, filename))

                                if max_count is not None and (num - start_num) >= max_count:
                                    reach_limit = True
                                    break
                        except Exception as e:
                            print(f"{self.category_name} Error occur")
                            print(e)

                    if reach_limit:
                        break
                driver.close()
                if reach_limit:
                    break
            if reach_limit:
                break


if __name__ == "__main__":
    WebCrawler("Train").run(["Train", "railway"])
