# Selenium functions will not be used directly, because if there are changes in the library functions in an update, it's more efficient if we just make the changes in this file than in the whole software.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def selenium_clear(element):
    element.clear()

def selenium_click(element):
    element.click()

def selenium_find_element(driver, css_selector):
    return driver.find_element(by = By.CSS_SELECTOR, value = css_selector)

def selenium_find_elements(driver, css_selector):
    return driver.find_elements(by = By.CSS_SELECTOR, value = css_selector)

def selenium_get_text(element):
    return element.text

def selenium_select(element):
    return Select(element)

def selenium_select_by_visible_text(element, text):
    element.select_by_visible_text(text)

def selenium_send_keys(element, text):
    element.send_keys(text)
