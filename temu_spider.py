import time
# import undetected_chromedriver as webdriver
from seleniumwire.undetected_chromedriver import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utils import _wait_for_element, upload_noteDday, generate_passwd, generate_ip
from fake_mail import MailServer
import requests
from loguru import logger
from bs4 import BeautifulSoup
import threading
import re


class Spider:
    def __init__(self, options, selenium_options, temu_spider_url, goods_index, tag, group_id):
        self.driver = webdriver.Chrome(options=options, selenium_options=selenium_options)
        self.goods_index = goods_index
        self.tag = tag
        self.group_id = group_id
        self.temu_spider_url = temu_spider_url
        self.temu_spider()

    def login(self, driver):
        mail_server = MailServer()
        mail = mail_server.get_mail()
        driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(mail)
        submit_btn = driver.find_element(By.ID, 'submit-button')
        driver.execute_script("arguments[0].click();", submit_btn)
        if _wait_for_element(driver, 'pwdInputInLoginDialog', 'id', 10):
            password = generate_passwd(8)
            logger.info(str(mail) + "_____" + str(password) + "\n")
            driver.find_element(By.ID, 'pwdInputInLoginDialog').send_keys(password)
            register_btn = driver.find_element(By.ID, 'submit-button')
            driver.execute_script("arguments[0].click();", register_btn)

    def temu_spider(self):
        self.driver.get('https://ipinfo.io')
        time.sleep(60)
        self.driver.get(self.temu_spider_url)
        self.login(self.driver)
        for _ in range(100):
            try:
                self.driver.find_element(By.XPATH, '//a[@index="{}" and @pageelsn="200064"]'.format(self.goods_index))
                break
            except Exception as e:
                time.sleep(1)
                continue
        for _ in range(2):
            url_list = []
            time.sleep(5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            for times in range(1000):
                try:
                    element = self.driver.find_element(By.XPATH, '//a[@index="{}" and @pageelsn="200064"]'.format(self.goods_index))
                    url_list.append(element.get_attribute('href'))
                    self.goods_index += 1
                except Exception as e:
                    # self.goods_spider_pool(url_list=url_list)
                    for url in url_list:
                        self.goods_item_spider_task(url)
                    self.driver.get(self.temu_spider_url)
                    for count in range(times):
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        elem_next = self.driver.find_element(By.XPATH,
                                                             '//span[text()="See more"]')
                        self.driver.execute_script("arguments[0].click();", elem_next)

    def goods_spider_pool(self, url_list):
        thread_arr = []
        for item_url in url_list:
            thread_arr.append(threading.Thread(target=self.goods_item_spider_task, args=(item_url, )))
        loop_num = int(len(thread_arr) / 10)
        for loop_index in range(loop_num + 1):
            if (loop_index + 1) * 10 < len(thread_arr):
                for thread_index in range(loop_index * 10, (loop_index + 1) * 10):
                    thread_arr[thread_index].start()
                for thread_index in range(loop_index * 10, (loop_index + 1) * 10):
                    thread_arr[thread_index].join()
            else:
                for thread_index in range(loop_index * 10, len(thread_arr)):
                    thread_arr[thread_index].start()
                for thread_index in range(loop_index * 10, len(thread_arr)):
                    thread_arr[thread_index].join()

    def extract_first_number_in_parentheses(self, text):
        pattern = r'\((\d+)\)'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None

    def goods_item_spider_task(self, url):
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless--')
        # driver = webdriver.Chrome(options=options)
        self.driver.get(url=url)
        # self.login(driver)
        # time.sleep(2)
        if _wait_for_element(self.driver, "//h2[@data-idx=0]", "XPATH", 10):
            review_sum_ele = self.driver.find_element(By.XPATH, "//h2[@data-idx=0]")
            total = self.extract_first_number_in_parentheses(review_sum_ele.text)
        else:
            return
        total = int(total)
        for page_index in range(int(total / 10)):
            if _wait_for_element(self.driver, '_244ldJXl', 'class', 10):
                product_name_element = self.driver.find_element(By.CLASS_NAME, '_2rn4tqXP')
                product_name = product_name_element.text
                price_element = self.driver.find_element(By.CLASS_NAME, '_3cZnvUvE')
                price_value = price_element.text[1:]
                review_items = self.driver.find_elements(By.CLASS_NAME, '_244ldJXl')
                for review_item in review_items:
                    item_html = review_item.get_attribute('innerHTML')
                    item_soup = BeautifulSoup(item_html, "html.parser")

                    # 提取图片数量和图片链接
                    image_divs = item_soup.find_all('div', class_='_370S0OXp')
                    image_count = len(image_divs)
                    image_links = [img.find('img')['src'] for img in image_divs]

                    if image_count > 0:
                        img_url = ''
                        for url in image_links:
                            url = url.replace("\"", "") + "___"
                            img_url = img_url + url

                        size_color_element = item_soup.find('div', class_="_1mxn2DUg")
                        review_size_color = size_color_element.get_text()

                        # 提取评论内容
                        review_div = item_soup.find('div', class_='_2EO0yd2j')
                        review_content = review_div.text.strip()

                        # 提取评分
                        rate_divs = item_soup.find_all('div', class_='_370S0OXp')
                        rating = len(rate_divs)

                        logger.info(
                            "ProductName: " + product_name + "\n" + "Price: " + price_value + "\n" + "Rate:" \
                            + rating + "\n" + "SizeColor: {}".format(review_size_color) + "\n" + \
                            "Body: {}".format(review_content) + "\n" + "img_url:" + img_url + "\n" + "-----" + "\n\n\n")
                    page_next_element = self.driver.find_element(By.XPATH, '//a[text()="{}"]'.format(page_index))
                    self.driver.execute_script("arguments[0].click();", page_next_element)



if __name__ == '__main__':
    url = 'https://www.temu.com/sports-outdoors-o3-178.html?opt_level=1&title=Sports%20%26%20Outdoors&show_search_type=0&refer_page_name=goods&refer_page_id=10032_1690870812603_wwde9bq5f5&refer_page_sn=10032&_x_sessn_id=o98ge9r1ib&is_back=1'
    ip = generate_ip()
    selenium_options = {
        'http': 'http://{}'.format(ip),
        'https': 'http://{}'.format(ip),
        'no_proxy': 'localhost,127.0.0.1'
    }
    options = webdriver.ChromeOptions()
    Spider(options=options,selenium_options= selenium_options, temu_spider_url=url, goods_index=0, tag='47,56,520', group_id=55)
