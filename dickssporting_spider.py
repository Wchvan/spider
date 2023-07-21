import time
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utils import _wait_for_element, upload_noteDday
import requests
from loguru import logger
from bs4 import BeautifulSoup
import threading
import re


class Spider:
    def __init__(self, options, spider_url, goods_index):
        self.driver = webdriver.Chrome(options)
        self.goods_index = goods_index
        self.spider_url = spider_url
        self.sports_spider(spider_url, goods_index)

    def get_goods_links(self):
        if (_wait_for_element(self.driver, 'image', 'class', 10)):
            time.sleep(10)
            goods_elements = self.driver.find_elements(By.CLASS_NAME, 'image')
            goods_links = []
            for element in goods_elements:
                goods_links.append(element.get_attribute('href'))
            return goods_links
        raise TimeoutError('无法找到链接')

    def sports_spider(self, url, goods_index):
        self.driver.get(url)
        goods_links = self.get_goods_links()
        for index in range(self.goods_index, len(goods_links)):
            try:
                # 采用浏览器的方式
                link = goods_links[index]
                link = link + "?bvstate=pg:2%2Fct:r"
                logger.info(goods_links)
                logger.info(link)
                self.goods_index = index + 1
                with open("break.txt", "a") as f:
                    f.write(str(self.spider_url) + "_____" + str(self.goods_index) + "\n")
                self.driver.get(link)
                time.sleep(10)
                self.driver.execute_script("window.scrollTo(0, 3500);")
                if (_wait_for_element(self.driver, "bv-content-summary-body-text", "class", 60)):
                    product_name_element = self.driver.find_element(By.XPATH, '//h1[@itemprop="name"]')
                    product_name = product_name_element.text
                    price_element = self.driver.find_element(By.CLASS_NAME, 'product-price')
                    price_value = price_element.text[1:]
                    reviews_elements = self.driver.find_elements(By.CLASS_NAME, 'bv-content-core ')
                    for reviews_element in reviews_elements:
                        item_html = reviews_element.get_attribute('innerHTML')
                        item_soup = BeautifulSoup(item_html, "html.parser")

                        # 找到评论的图片元素，并获取图片数量和链接
                        # 找到所有包含img元素的bv-media-item-photo元素
                        img_elements = item_soup.select('.bv-media-item-photo')
                        # 获取img元素的个数
                        num_images = len(img_elements)
                        # 获取img元素的链接
                        img_links = [img.select_one('img')['src'] for img in img_elements]
                        img_url = ''
                        for url in img_links:
                            url = url.replace("\"", "") + "___"
                            img_url = img_url + url
                        logger.info(num_images)
                        if num_images >= 1:
                            logger.info("获取到有效评论信息")

                            # 找到评论的评分元素，并获取评分星数
                            rating_element = item_soup.find(class_='bv-rating-max')
                            rating = rating_element['title'].split()[0] if rating_element else None

                            # 找到评论的标题和内容元素
                            title_element = item_soup.find(class_='bv-content-title')
                            content_element = item_soup.find(class_='bv-content-summary-body-text')
                            review_title = title_element.text.strip() if title_element else None
                            review_content = content_element.text.strip() if content_element else None

                            with open("reviews.txt", "a") as f:
                                f.write(
                                    "ProductName: " + product_name + "\n" + "Price: " + price_value + "\n" + "Rate:" \
                                    + rating + "\n" + "Title: {}".format(review_title) + "\n" + \
                                    "Body: {}".format(review_content) + "\n" + "img_url:" + img_url + "\n" + "-----" + "\n\n\n")
                                upload_noteDday(review_title, review_content, price_value, rating, product_name, urls,
                                                '47,51,500', 42)
            except Exception as e:
                continue

        time.sleep(1)
        self.driver.close()


def spider_task(url, page, page_size, goods_index):
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        spider_url = url + str(page * page_size)
        Spider(options, spider_url, goods_index)
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
   urls = ["https://www.dickssportinggoods.com/f/baseball-bats?pageNumber="]
   for url in urls:
       # 设置每个线程处理的页面范围
       page_1 = 0
       page_2 = 1
       page_3 = 2
       page_4 = 3
       # page_5 = 4

       # 创建线程
       thread1 = threading.Thread(target=spider_task, args=(url, page_1, 1, 0))
       thread2 = threading.Thread(target=spider_task, args=(url, page_2, 1, 0))
       thread3 = threading.Thread(target=spider_task, args=(url, page_3, 1, 0))
       thread4 = threading.Thread(target=spider_task, args=(url, page_4, 1, 0))
       # thread5 = threading.Thread(target=spider_task, args=(url, page_5, 1, 0))

       # 启动线程
       thread1.start()
       thread2.start()
       thread3.start()
       thread4.start()
       # thread5.start()

       # 等待所有线程结束
       thread1.join()
       thread2.join()
       thread3.join()
       thread4.join()
       # thread5.join()

