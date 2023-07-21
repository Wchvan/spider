from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random
from loguru import logger
from time import sleep
from note import Note

def _random_sleep(minimum=10, maximum=20):
    t = random.randint(minimum, maximum)
    logger.info(f'Wait {t} seconds')
    sleep(t)

def _is_element_present(driver, how, what):
    """Check if an element is present"""
    try:
        driver.find_element(by=how, value=what)
        return True
    except NoSuchElementException:
        return False

def _wait_for_element(driver, element_tag, locator, timeout=30):
    """Wait till element present. Max 30 seconds"""
    locator = locator.upper()
    for i in range(timeout):
        try:
            if locator == 'ID' and _is_element_present(driver, By.ID, element_tag):
                return True
            elif locator == 'NAME' and _is_element_present(driver, By.NAME, element_tag):
                return True
            elif locator == 'TAG_NAME' and _is_element_present(driver, By.TAG_NAME, element_tag):
                return True
            elif locator == 'XPATH' and _is_element_present(driver, By.XPATH, element_tag):
                return True
            elif locator == 'CSS' and _is_element_present(driver, By.CSS_SELECTOR, element_tag):
                return True
            elif locator == 'CLASS' and _is_element_present(driver, By.CLASS_NAME, element_tag):
                return True
            else:
                logger.warning(f"Element {element_tag} is not found! type is {locator}.")
        except Exception as e:
            logger.error("Wait time error: {}".format(e))
        _random_sleep(1, 2)
    logger.info(f"Timed out. Element not found with {locator} : {element_tag}")
    return False


def upload_noteDday(titleraw, contentraw, price, rating, productname, img, tag, groupid):
    note = Note()
    note.title_raw = titleraw
    note.content_raw = contentraw
    note.extend = price
    note.rate = rating
    note.product_name = productname
    note.files = img
    note.tag = tag
    note.origin_files = img

    note.upload_new_note(note_group_id=groupid)
