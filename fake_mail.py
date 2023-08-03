import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


# from requests.packages import urllib3
class MailServer:

    def __init__(self):
        pass

    def get_mail(self):
        url = "https://email-fake.com/"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        # req = requests.get(url)
        # soup = BeautifulSoup(req.content, "html.parser")
        # mail = soup.find_all("span", {"id": "email_ch_text"})
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        div = driver.find_element(By.ID, 'email_ch_text')
        email = div.text
        driver.close()

        return email

    def get_mail_code(self, mail_name, mail_type):

        INST_CODE = 'https://email-fake.com/' + mail_name
        #
        # driver.execute_script("window.open('');")
        # driver.switch_to.window(driver.window_handles[1])
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(INST_CODE)

        # button = browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/table/tbody/tr[3]/td[1]/a/button").click()
        # time.sleep(3)
        t = driver.title
        flag = 0
        while True:
            if t[:4] == "Fake":
                driver.refresh()
                t = driver.title
                print(t)
                time.sleep(1)
                flag += 1
                print(t)
                if flag == 30:
                    return -1
            else:
                break
        # code = browser.find_element_by_xpath("//*[@id='email-table']/div[2]/div[1]/div/h1").text
        # code = code.replace("is your Instagram code", "")
        if mail_type == 'Facebook':
            code = t[3:8]
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            return code
        else:
            code = t[:7]
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            return code


if __name__ == '__main__':
    MailServer = MailServer()
    res = MailServer.get_mail()
    print(res)
    code = MailServer.get_mail_code(res, "Facebook")
    print(code)