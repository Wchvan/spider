import undetected_chromedriver as webdriver
# from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import _wait_for_element
from loguru import logger
from bs4 import BeautifulSoup
import threading
import string
import csv
import http.client
import json


def LaGuardia_spider_task(letter):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get('https://apps.laguardia.edu/directory/')
    if _wait_for_element(driver, 'txtFirstName', 'id', 10):
        first_name_input = driver.find_element(By.ID, 'txtFirstName')
        first_name_input.send_keys(letter)
        confirm_button = driver.find_element(By.NAME, 'txtSearch')
        driver.execute_script("arguments[0].click();", confirm_button)
        if _wait_for_element(driver, 'outputDataGrid', 'id', 10):
            table_element = driver.find_element(By.ID, 'outputDataGrid')
            teacher_data = []
            soup = BeautifulSoup(table_element.get_attribute('innerHTML'), 'html.parser')

            # Iterate through each row in the table
            for row in soup.find_all('tr')[1:]:  # Skip the header row (index 0)
                columns = row.find_all('td')

                # Extract the desired information (First Name, Last Name, and Email)
                first_name = columns[0].text.strip()
                last_name = columns[1].text.strip()
                email = columns[6].text.strip()

                # Append the data as a tuple to the teacher_data list
                teacher_data.append((first_name, last_name, email))

            # Write the data to a CSV file
            with open('teacher.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['First Name', 'Last Name', 'Email'])  # Write header row
                csv_writer.writerows(teacher_data)  # Write the extracted data rows
            driver.close()


def BMCC_spider_tast(letter):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.bmcc.cuny.edu/directory/')
    if _wait_for_element(driver, 'first-name', 'id', 10):
        first_name_input = driver.find_element(By.ID, 'first-name')
        first_name_input.send_keys(letter)
        confirm_button = driver.find_element(By.XPATH, '//button[text()="Search"]')
        driver.execute_script("arguments[0].click();", confirm_button)
        if _wait_for_element(driver, 'entry-content', 'class', 10):
            table_element = driver.find_element(By.CLASS_NAME, 'entry-content')
            teacher_data = []
            soup = BeautifulSoup(table_element.get_attribute('innerHTML'), 'html.parser')

            person_entries = soup.find_all('div', class_='dir-person-list-entry')

            # Iterate through each person entry and extract the desired information
            for person in person_entries:
                try:
                    name_element = person.find('div', class_='dir-person-name')
                    first_name, last_name = name_element.h3.text.strip().split(maxsplit=1)

                    email_element = person.find('div', class_='dir-person-email')
                    email = email_element.find('span', class_='dir-field-title').find_next_sibling('span').text.strip()

                    teacher_data.append([first_name, last_name, email])
                except Exception as e:
                    continue

            # Write the data to a CSV file
            output_file = "teacher.csv"
            with open(output_file, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(teacher_data)  # Write the extracted data rows

            driver.close()


def Bronx_spider(letter):
    conn = http.client.HTTPSConnection("ra.bcc.cuny.edu")
    payload = '{{"fname": "John", "lname": "Doe", "deptID": "", "ch": "{}", "func": "", "phExt": ""}}'.format(letter)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'ra.bcc.cuny.edu',
        'Connection': 'keep-alive'
    }
    conn.request("POST", "/BCCAPI/Service.asmx/GetBCCEmplDirectorySearch", payload, headers)
    res = conn.getresponse()
    data = res.read()
    res_str = data.decode("utf-8")

    # 解析 JSON 响应
    json_data = json.loads(res_str)

    # 提取字段并保存到CSV文件
    with open('teacher.csv', 'a', newline='') as csvfile:
        fieldnames = ['First Name', 'Last Name', 'Email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for employee in json_data['d']:
            full_name = employee['EMPL_NAME']
            first_name, last_name = full_name.split(', ', 1)
            email = employee['EMPL_EMAIL']

            writer.writerow({'First Name': first_name, 'Last Name': last_name, 'Email': email})


def Stella_spider_task():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get('https://guttman.cuny.edu/about/directory/#offices')
    if _wait_for_element(driver, "vc_tta-panel-body", "class", 10):
        table_element = driver.find_element(By.CLASS_NAME, 'vc_tta-panel-body')
        soup = BeautifulSoup(table_element.get_attribute('innerHTML'), 'html.parser')
        with open('teacher.csv', 'w', newline='') as csvfile:
            fieldnames = ['First Name', 'Last Name', 'Email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # 查找所有的h3标签，这里假设所有的h3标签都包含了名字信息
            h3_tags = soup.find_all('h3')

            for h3_tag in h3_tags:
                try:
                    # 获取名字信息
                    full_name = h3_tag.get_text()
                    first_name, last_name = full_name.split(' ', 1)

                    # 获取邮箱信息
                    email_tag = h3_tag.find_next('a')
                    email = email_tag['href'].split(':')[1]

                    # 写入CSV文件
                    writer.writerow({'First Name': first_name, 'Last Name': last_name, 'Email': email})
                except Exception as e:
                    continue
    driver.get('https://guttman.cuny.edu/about/directory/#fsa')
    if _wait_for_element(driver, "GuttmanDirectory_wrapper", "id", 10):
        table_element = driver.find_element(By.XPATH, "//tbody")
        soup = BeautifulSoup(table_element.get_attribute('innerHTML'), 'html.parser')
        # 提取字段并保存到CSV文件
        with open('teacher.csv', 'a', newline='') as csvfile:
            fieldnames = ['First Name', 'Last Name', 'Email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # 查找所有的tr标签
            rows = soup.find_all('tr')
            for row in rows:
                # 查找h2标签，并获取名字
                name_tag = row.find('h2')
                full_name = name_tag.get_text()
                first_name, last_name = full_name.split(' ', 1)
                # 查找a标签，并获取邮箱
                email_tag = row.find('a')
                email = email_tag['href'].split(':')[1]
                # 写入CSV文件
                writer.writerow({'First Name': first_name, 'Last Name': last_name, 'Email': email})


def Kingsborough_spider():
    html_data = """请输入html"""

    # 解析HTML数据
    soup = BeautifulSoup(html_data, "html.parser")

    # 提取字段并保存到CSV文件
    with open('teacher.csv', 'a', newline='') as csvfile:
        fieldnames = ['First Name', 'Last Name', 'Email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # 查找所有的<tbody>标签中的<tr>标签，这里假设每个<tr>标签都包含了一个人的信息
        rows = soup.select('tbody tr')

        for row in rows:
            # 获取姓名信息
            name_cell = row.select_one('td:nth-of-type(1)')
            full_name = name_cell.get_text()
            first_name, last_name = full_name.split(' ', 1)

            # 获取邮箱信息
            email_cell = row.select_one('td:nth-of-type(2)')
            email = email_cell.get_text()

            # 写入CSV文件
            writer.writerow({'First Name': first_name, 'Last Name': last_name, 'Email': email})


if __name__ == '__main__':
    thread_arr = []
    uppercase_letters = string.ascii_uppercase
    # Stella_spider_task()
    Kingsborough_spider()
    # for letter in uppercase_letters:
        # LaGuardia_spider_task(letter)
        # BMCC_spider_tast(letter)
        # Bronx_spider(letter)
