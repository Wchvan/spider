import requests
from loguru import logger
from urllib.parse import quote
import json
from utils import get_correct_proxies, upload_noteDday
import urllib3
import threading

urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5
home_url = "https://prod-catalog-product-api.dickssportinggoods.com/v2/search?searchVO="
review_url = "https://api.bazaarvoice.com/data/reviews.json?passkey=cahWEzSiPp0IPkqzl0gm4jqVhsyCj0T2DLPYonOqIqDoc&apiVersion=5.4&Include=Products&Stats=Reviews&filter=productId:{}&Include=Products&Stats=Reviews"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

proxy = get_correct_proxies()


class Spider:
    def __init__(self, selected_category, store_id, page_number, goods_index, tag, group_id):
        self.goods_index = goods_index
        self.tag = tag
        self.group_id = group_id
        self.params = {
            "selectedCategory": selected_category,
            "selectedStore": "0",
            "selectedSort": 5,
            "selectedFilters": {},
            "storeId": store_id,
            "pageNumber": page_number,
            "pageSize": 48,
            "totalCount": 0,
            "searchTypes": ["PINNING"],
            "isFamilyPage": True,
            "snbAudience": "",
            "zipcode": "90245"
        }

        try:
            url = home_url + quote(json.dumps(self.params))
            response = requests.get(url, proxies=proxy, headers=headers, verify=False)
            product_list = response.json()["productVOs"]
            logger.info(len(product_list))
            for index in range(self.goods_index, len(product_list)):
                with open("break.txt", "a") as f:
                    logger.info(str(selected_category) + "____" + str(store_id) + "____" + str(self.goods_index))
                    f.write(str(selected_category) + "____" + str(store_id) + "____" + str(self.goods_index) + "\n")

                product = product_list[index]
                product_name = product["name"]
                product_price = str(product["floatFacets"][1]["stringValue"])
                product_id = product["thumbnail"]
                try:
                    self.goods_index = index + 1
                    self.sports_spider(product_id, product_name, product_price)
                except Exception as e:
                    logger.error(e)
        except Exception as e:
            logger.error(e)

    def sports_spider(self, product_id, product_name, product_price):
        url = review_url.format(product_id)
        try:
            response = requests.get(url, proxies=proxy, headers=headers, verify=False)
            review_list = response.json()['Results']
            for review in review_list:
                if len(review['Photos']) >= 1 and not str(review["ReviewText"]).startswith('[This review was collected as part of a promotion.]'):
                    logger.info('有效评论')
                    review_title = review["Title"]
                    rating = str(review["Rating"])
                    review_content = review["ReviewText"]
                    photo_url = ''
                    for photo_item in review['Photos']:
                        photo_url = photo_url + photo_item["Sizes"]["thumbnail"]["Url"] + "___"
                    logger.info(photo_url)
                    logger.info("ProductName: " + product_name + "\n" + "Price: " + product_price + "\n" + "Rate:" \
                                + rating + "\n" + "Title: {}".format(review_title) + "\n" + \
                                "Body: {}".format(review_content) + "\n" + "img_url:" + photo_url \
                                + "\n" + "-----" )
                    with open("reviews.txt", "a") as f:
                        f.write(
                            "ProductName: " + product_name + "\n" + "Price: " + product_price + "\n" + "Rate:" \
                            + rating + "\n" + "Title: {}".format(review_title) + "\n" + \
                            "Body: {}".format(review_content) + "\n" + "img_url:" + photo_url \
                            + "\n" + "-----" + "\n\n\n")
                        upload_noteDday(review_title, review_content, product_price, rating, product_name,
                                        photo_url, self.tag, self.group_id)
        except Exception as e:
            logger.error(e)


def spider_task(selected_category, store_id, page_number, goods_index, tag, group_id):
    try:
        Spider(selected_category, store_id, page_number, goods_index, tag, group_id)
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    store_id = 15108
    tag = '47,57,500'
    group_id = 50
    # https://www.dickssportinggoods.com/f/volleyball-training
    selected_category_list = ['12301_277645', '12301_201724', '12301_201709']
    page_list = [4, 3, 2, ]
    thread_arr = []

    for index in range(len(selected_category_list)):
        for page in range(page_list[index]):
            thread_arr.append(threading.Thread(target=spider_task, args=(selected_category_list[index], store_id, page, 0, tag, group_id)))

    loop_num = int(len(thread_arr) / 10)
    for loop_index in range(loop_num + 1):
        if (loop_index+1) * 10 < len(thread_arr):
            for thread_index in range(loop_index * 10, (loop_index+1)*10):
                thread_arr[thread_index].start()
            for thread_index in range(loop_index * 10, (loop_index + 1) * 10):
                thread_arr[thread_index].join()
        else:
            for thread_index in range(loop_index * 10, len(thread_arr)):
                thread_arr[thread_index].start()
            for thread_index in range(loop_index * 10, len(thread_arr)):
                thread_arr[thread_index].join()
