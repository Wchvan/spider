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
    def __init__(self, options, home_spider_url, goods_index):
        self.driver = webdriver.Chrome(options)
        self.goods_index = goods_index
        self.home_spider_url = home_spider_url
        self.home_spider(home_spider_url, goods_index)

    def home_goods_links(self):
        if (_wait_for_element(self.driver, 'product-image', 'class', 10)):
            self.driver.execute_script("window.scrollTo(0, 2000);")
            time.sleep(15)
            self.driver.execute_script("window.scrollTo(0, 4000);")
            time.sleep(15)
            self.driver.execute_script("window.scrollTo(0, 6000);")
            time.sleep(15)
            self.driver.execute_script("window.scrollTo(0, 8000);")
            time.sleep(15)
            goods_elements = self.driver.find_elements(By.CLASS_NAME, 'product-image')
            goods_links = []
            for element in goods_elements:
                goods_links.append(element.get_attribute('href'))
            return goods_links
        raise TimeoutError('无法找到链接')

    def reviews_button(self):
        if (_wait_for_element(self.driver, 'ratings-and-reviews-accordion-title', 'id', 10)):
            button = self.driver.find_element(By.ID, 'ratings-and-reviews-accordion-title')
            self.driver.execute_script("arguments[0].click();", button)

    def home_spider(self, url, goods_index):
        self.driver.get(url)
        goods_links = self.home_goods_links()
        logger.info(len(goods_links))
        for index in range(self.goods_index, len(goods_links)):
            # 采用浏览器的方式
            link = goods_links[goods_index]
            self.goods_index += 1
            with open("break.txt", "a") as f:
                f.write(str(self.home_spider_url) + "_____" + str(self.goods_index) + "\n")

            self.driver.get(link)
            for _ in range(2):
                try:
                    if (_wait_for_element(self.driver, "price-format__large", "class", 10)):
                        product_name_element = self.driver.find_element(By.CLASS_NAME,
                                                                        'product-details__badge-title--wrapper')
                        product_name = product_name_element.text
                        price_element = self.driver.find_element(By.CLASS_NAME, "price")
                        # 使用BeautifulSoup解析元素的HTML内容
                        soup = BeautifulSoup(price_element.get_attribute('outerHTML'), "html.parser")
                        # 选择所有子元素
                        price_children = soup.find("div",
                                                   class_="price-format__large price-format__main-price").find_all(
                            recursive=False)
                        # 提取价格数值
                        price_value = "".join(item.text for item in price_children if item.name == "span")
                        price_value = price_value.replace("$", "")
                        logger.info(price_value)
                        break
                    else:
                        self.driver.refresh()
                except Exception as e:
                    self.driver.refresh()

            # 查找"/p/"后面的索引位置
            index_after_p = link.find("/p/") + 3
            # 获取"/p/"后面的部分，即产品编号
            product_url = link[index_after_p:]
            # 构建包含"reviews"的新URL
            reviews_url = f"https://www.homedepot.com/p/reviews/{product_url}"

            for index in range(1, 16):
                try:
                    self.driver.get(reviews_url + "/" + str(index))
                    if (_wait_for_element(self.driver, "review_item", "class", 10)):
                        review_items = self.driver.find_elements(By.CLASS_NAME, 'review_item')
                        for review_item in review_items:
                            item_html = review_item.get_attribute('innerHTML')
                            item_soup = BeautifulSoup(item_html, "html.parser")

                            # 提取review-content__title
                            title_element = item_soup.select_one(".review-content__title")
                            review_title = title_element.get_text()

                            # 提取review-content-body
                            body_element = item_soup.select_one(".review-content-body")
                            review_body = body_element.get_text()

                            # 提取media-carousel__media的数量
                            media_elements = item_soup.select(".media-carousel__media")
                            media_count = len(media_elements)

                            # 提取评分
                            stars_element = item_soup.select_one(".stars--c43xm")
                            width_style = stars_element.get("style")
                            width_percentage = width_style.split("width: ")[1].split("%;")[0]
                            rating = str(int((float(width_percentage) / 100) * 5))  # 将百分比转换为1-5的评分

                            # 打印提取的结果
                            if media_count >= 1:
                                img_urls = []
                                for media_element in media_elements:
                                    image_button = media_element.select_one("button")
                                    image_url = image_button["style"].split("url(")[-1].split(")")[0].replace("&quot;",
                                                                                                              "")
                                    img_urls.append(image_url)

                                urls = ""
                                for url in img_urls:
                                    url = url.replace("\"", "") + "___"
                                    urls = urls + url
                                logger.info("获取到有效评论信息")

                                with open("reviews.txt", "a") as f:
                                    f.write(
                                        "ProductName: " + product_name + "\n" + "Price: " + price_value + "\n" + "Rate:" \
                                        + rating + "\n" + "Title: {}".format(review_title) + "\n" + \
                                        "Body: {}".format(
                                            review_body) + "\n" + "img_url:" + urls + "\n" + "-----" + "\n\n\n")
                                    upload_noteDday(review_title, review_body, price_value, rating, product_name, urls,
                                                    '58,60,500', 28)
                    else:
                        break
                except Exception as e:
                    index -= 1
                    logger.error(e)
        time.sleep(1)
        self.driver.close()


def spider_task(url, page, page_size, goods_index):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        home_spider_url = url + str(page * page_size)
        Spider(options, home_spider_url, goods_index)
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
   urls = ["https://www.homedepot.com/b/Bath-Bathroom-Accessories-Bathroom-Hardware/N-5yc1vZcfv8?Nao="]
   for url in urls:
       # 设置每个线程处理的页面范围
       page_1 = 0
       page_2 = 1
       page_3 = 2
       page_4 = 3
       page_5 = 4

       # 创建线程
       thread1 = threading.Thread(target=spider_task, args=(url, page_1, 24, 0))
       thread2 = threading.Thread(target=spider_task, args=(url, page_2, 24, 0))
       thread3 = threading.Thread(target=spider_task, args=(url, page_3, 24, 0))
       thread4 = threading.Thread(target=spider_task, args=(url, page_4, 24, 0))
       thread5 = threading.Thread(target=spider_task, args=(url, page_5, 24, 0))

       # 启动线程
       thread1.start()
       thread2.start()
       thread3.start()
       thread4.start()
       thread5.start()

       # 等待所有线程结束
       thread1.join()
       thread2.join()
       thread3.join()
       thread4.join()
       thread5.join()

