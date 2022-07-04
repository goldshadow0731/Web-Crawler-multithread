from base64 import b64decode
import os
import time
from typing import Text, List, Union
# from urllib.request import urlretrieve, urlopen
import requests

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class WebCrawler():
    default_file_ext = 'jpg'
    roll_down_unit = 500
    roll_down_times = 100
    chrome_driver = f'{os.getcwd()}/chromedriver/chromedriver'

    def __init__(self, id=None):
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = Chrome(service=Service(
            self.chrome_driver), options=chrome_options)
        # self.driver.maximize_window()
        self.id = id

    def __del__(self):
        self.driver.close()

    def crawler_image(self, search_url: Text, save_name_format: Text, xpath_value: Text, save_path: Text = './images', num: int = 0, max_count: Union[None, int] = None, verbose: int = 1) -> None:
        """_summary_

        Args:
            search_url (Text): _description_
            save_name_format (Text): _description_
            xpath_value (Text): _description_
            save_path (Text, optional): _description_. Defaults to './images'.
            num (int, optional): _description_. Defaults to 0.
            max_count (Union[None, int], optional): _description_. Defaults to None.
            verbose (int, optional): _description_. Defaults to 1.
        """
        start_num = num
        reach_limit = False
        os.makedirs(save_path, exist_ok=True)

        self.driver.get(search_url)  # searching

        for k in range(self.roll_down_times):  # load more result
            if verbose >= 2:
                if self.id is not None:
                    print(f'ID: {self.id:>2d}', end=' ')
                print(f'Roll down: {k}')

            # roll down
            self.driver.execute_script(
                f'document.documentElement.scrollTop={k * self.roll_down_unit}')

            # get image
            for element in self.driver.find_elements(by=By.XPATH, value=xpath_value):
                try:
                    img_url = element.get_attribute('src')  # get image source
                    if img_url is not None:  # save image
                        filename = save_name_format.format(num=num)
                        # e.g., data:image/jpeg;base64,<base64 image ...>
                        if img_url.startswith('data:image'):
                            head, data = img_url.split(',', 1)
                            file_ext = head.split(';')[0].split('/')[1]
                            file_path = os.path.join(save_path,
                                                     f'{filename}.{file_ext}')
                            with open(file_path, 'wb') as fp:
                                fp.write(b64decode(data))
                        elif img_url.startswith('http'):
                            file_path = os.path.join(
                                save_path, f'{filename}.{self.default_file_ext}')
                            with requests.get(img_url, timeout=(3, 7), stream=True) as r:
                                r.raise_for_status()
                                with open(file_path, 'wb') as fp:
                                    for chunk in r.iter_content(chunk_size=4096):
                                        fp.write(chunk)
                except Exception as e:
                    if verbose >= 2:
                        if self.id is not None:
                            print(f'ID: {self.id:>2d}', end=' ')
                        print(f'Error: {e}' if verbose >=
                              3 else f'Error occur')
                    else:
                        pass
                else:
                    if verbose >= 1:
                        if self.id is not None:
                            print(f'ID: {self.id:>2d}', end=' ')
                        print(f'Filename: {filename:>10s}')

                    num += 1
                    if max_count is not None and (num - start_num) >= max_count:
                        reach_limit = True
                        break

                    time.sleep(1)

            if reach_limit:
                break


if __name__ == '__main__':
    search_engine = {
        "google": {
            "url": "https://www.google.com.tw/search?q={keyword}&tbm=isch&ved=2ahUKEwiwvsi-y5_tAhVH4GEKHe5JBUwQ2-cCegQIABAA&oq=%E8%B2%93&gs_lcp=CgNpbWcQAzIECCMQJzIECCMQJzIFCAAQsQMyBQgAELEDMgUIABCxAzIFCAAQsQMyAggAMgUIABCxAzICCAAyBQgAELEDOgcIIxDqAhAnUN0WWJseYPkhaAFwAHgBgAG3AYgBugWSAQMwLjWYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCsABAQ&sclient=img&ei=KEy_X7CKE8fAhwPuk5XgBA&authuser=0&bih=687&biw=1455&hl=zh-TW",
            "xpath": '//div[@id="islrg"]/div/div/a/div/img'
        },
        "bing": {
            "url": "https://www.bing.com/images/search?q={keyword}&form=HDRSC2&first=1&scenario=ImageBasicHover&cw=1117&ch=864",
            "xpath": '//div[@id="b_content"]/div[@id="vm_c"]/div[@class="dg_b"]/div/ul/li/div/div/a/div[@class="img_cont hoff"]/img'
        },
        "sogou": {
            "url": "https://pic.sogou.com/pics?query={keyword}&di=2&_asf=pic.sogou.com&w=05009900",
            "xpath": '//div[@class="figure-result"]/ul/li/div/a/img'
        },
        "baidu": {
            "url": "http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word={keyword}",
            "xpath": '//div[@id="imgid"]/div/ul/li/div/div/a/img'
        },
        "360": {
            "url": "https://image.so.com/i?q={keyword}&src=tab_www",
            "xpath": '//div[@class="stream"]/div/div/div/ul/li/div/a/span/img'
        }
    }

    crawler = WebCrawler()
    crawler.crawler_image(
        search_engine['google']['url'].format(keyword='train'),
        save_name_format='{num:04d}_train',
        xpath_value=search_engine['google']['xpath'],
        save_path='./images/Train',
        max_count=10)
