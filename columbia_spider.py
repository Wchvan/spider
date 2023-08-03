import urllib
from utils import _wait_for_element
import loguru
from bs4 import BeautifulSoup
import csv
from faker import Faker
from selenium.webdriver.common.by import By
import undetected_chromedriver as webdriver
import string

fake = Faker()

def spider_task(name):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get('https://directory.columbia.edu/people/search')
    if _wait_for_element(driver, 'newSearch', 'id', 10):
        input = driver.find_element(By.ID, 'newSearch')
        input.send_keys(name)
        button = driver.find_element(By.XPATH, '//input[@value="Search"]')
        driver.execute_script("arguments[0].click();", button)
        if _wait_for_element(driver, 'table_results', 'class', 10):
            result = driver.find_element(By.CLASS_NAME, 'table_results')
            return result.get_attribute('innerHTML')
    driver.close()

# 提取姓名和电子邮件
def extract_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # 跳过表头行

    data = []
    for row in rows:
        columns = row.find_all('td')
        if len(columns) == 4:
            try:
                full_name = columns[0].find('a').get_text(strip=True)
                email = columns[3].find('a').text.strip()
                first_name, last_name = full_name.split(', ', 1)
                data.append([first_name, last_name, email])
            except Exception as e:
                continue

    return data

# 生成CSV文件
def generate_csv(data, output_file):
    with open(output_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['First Name', 'Last Name', 'Email'])
        writer.writerows(data)

# 主函数
def main(name):
    html_text = spider_task(name)
    data = extract_info(html_text)

    teacher_data = [row for row in data if 'student' not in row[2].lower()]
    student_data = [row for row in data if 'student' in row[2].lower()]

    generate_csv(teacher_data, 'teacher.csv')
    generate_csv(student_data, 'student.csv')

if __name__ == '__main__':
    first_name = fake.first_name()
    uppercase_letters = string.ascii_uppercase
    for letter in uppercase_letters:
        main(letter)