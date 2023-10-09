# Selenium functions will not be used directly, because if there are changes in the library functions in an update, it's more efficient if we just make the changes in this file than in the whole software.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException

class Selenium:
    def __init__(self):
        self.driver = webdriver.Edge()
    
    def clear(self, element):
        element.clear()

    def click(self, element):
        element.click()

    def click_loop(self, css_selector):
        while True:
            try:
                self.driver.find_element(by = By.CSS_SELECTOR, value = css_selector).click()
                break
            except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException, AttributeError):
                pass

    def fill_loop(self, css_selector, text): # Fill in a field or upload a file.
        while True:
            try:
                self.driver.find_element(by = By.CSS_SELECTOR, value = css_selector).send_keys(text)
                break
            except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, AttributeError):
                pass

    def find_element(self, css_selector):
        return self.driver.find_element(by = By.CSS_SELECTOR, value = css_selector)

    def find_elements(self, css_selector):
        return self.driver.find_elements(by = By.CSS_SELECTOR, value = css_selector)

    def get_page(self, page_url):
        self.driver.get(page_url)

    def get_text(self, element):
        return element.text

    def refresh(self):
        self.driver.refresh()

    def script(self, code):
        self.driver.execute_script(code)

    def select(self, element):
        return Select(element)

    def select_by_visible_text(self, element, text):
        element.select_by_visible_text(text)

    def send_keys(self, element, text):
        element.send_keys(text)

    def switch_to_window(self, window_index):
        self.driver.switch_to.window(self.driver.window_handles[window_index])

    def wait_for_element_to_appear(self, css_selector):
        while True:
            try:
                self.find_element(css_selector)
                break
            except:
                pass

    def wait_for_element_to_disappear(self, css_selector):
        while True:
            try:
                self.find_element(css_selector)
            except:
                break