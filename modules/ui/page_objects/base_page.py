from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchWindowException, TimeoutException,
                                        StaleElementReferenceException, NoSuchElementException, WebDriverException)
from selenium.webdriver.common.action_chains import ActionChains
from modules.common.webdriver_factory import get_driver

class BasePage:

    def __init__(self) -> None:

        self.driver = get_driver()

    def open(self, url):
        return self.driver.get(url)

    def close(self):
        self.driver.quit()

    # def switch_to_handle(self):
    #     for handle in self.driver.window_handles:
    #         self.driver.switch_to.window(handle)
    #         if self.driver.current_url == self.URL + "/":
    #             break

    def switch_current_handle(self, url):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if self.driver.current_url == url:
                break

    def switch_to_new_tab(self, element):
        url = self.get_attribute_value(element, "href")
        self.driver.switch_to.new_window('Tab')
        self.driver.get(url)
        # self.switch_current_handle(url)

    def element_is_visible(self, locator, timeout=10):
        try:
            element = WebDriverWait(driver=self.driver, timeout=timeout).until(

                EC.visibility_of_element_located(locator=locator))
            return element
        except (NoSuchWindowException, TimeoutException):
            return False

    def elements_are_visible(self, locator, timeout=30):
        try:
            elements = WebDriverWait(driver=self.driver, timeout=timeout).until(

                EC.visibility_of_all_elements_located(locator=locator))
            return elements
        except (NoSuchWindowException, TimeoutException):
            return False

    def element_is_present(self, locator, timeout=30):
        try:
            element = WebDriverWait(driver=self.driver, timeout=timeout).until(

                EC.presence_of_element_located(locator=locator))
            return element
        except TimeoutException:
            return False

    def elements_are_present(self, locator, timeout=30):
        try:
            element = WebDriverWait(driver=self.driver, timeout=timeout).until(

                EC.presence_of_all_elements_located(locator=locator))
            return element
        except TimeoutException:
            return False

    def element_is_clickable(self, locator, timeout=30):
        try:
            element = WebDriverWait(driver=self.driver, timeout=timeout).until(

                EC.element_to_be_clickable(locator))
            return element
        except (NoSuchElementException, TimeoutException):
            return False

    def element_is_relocated(self, locator):
        while True:
            try:
                element = self.element_is_visible(locator=locator)
                return element
            except StaleElementReferenceException:
                pass

    def click_on_button(self, element):
        self.driver.execute_script("arguments[0].click()", element)

    def move_to_element(self, argument):
        self.driver.execute_script("arguments[0].scrollIntoView();", argument)

    def close_promo_banner(self):
        self.driver.execute_script("document.getElementsByClassName\
        ('promocode-popup__close close-btn')[0].click();")

    def scroll_down(self, number_px):
        self.driver.execute_script(f"window.scrollTo(0, {number_px});")

    def get_attribute_value(self, element, attribute_name):
        return element.get_attribute(attribute_name)

    def title_is_present(self, title, timeout=30):
        try:
            state = WebDriverWait(self.driver, timeout).until(EC.title_contains(title))
            return state
        except (NoSuchElementException, TimeoutException):
            return False

    def element_is_not_present(self, locator):
        while True:
            try:
                element = self.element_is_present(locator)
                return element
            except StaleElementReferenceException:
                print('Element is not attached to page',
                      'Needed to wait',
                      'Trying again', sep='\n')

    def wait_load_page_after_refresh(self):
        self.driver.execute_script("window.onload= () => {log.console('DOM loaded')};")

    def move_to_elem(self, elem):
        ActionChains(self.driver).move_to_element(elem).click_and_hold(elem).perform()
