import logging

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchWindowException, TimeoutException,
                                        StaleElementReferenceException, NoSuchElementException, WebDriverException, NoAlertPresentException)
from selenium.webdriver.common.action_chains import ActionChains
from modules.common.webdriver_factory import get_driver
from selenium.webdriver.remote.webelement import WebElement


CORE_DIR = Path(__file__).resolve().parent.parent.parent.parent

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
handler = logging.FileHandler(CORE_DIR / f"data/{__name__}.log", mode='a')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
LOGGER.addHandler(handler)


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

    def switch_to_new_tab(self, url: str):
        current_handles = self.driver.window_handles
        self.driver.switch_to.new_window('Tab')
        self.driver.get(url)
        # self.switch_current_handle(url)
        return self.is_new_window_opened(current_handles)


    def element_is_visible(self, locator, timeout=10):
        try:
            element = WebDriverWait(driver=self.driver, timeout=timeout).until(
                EC.visibility_of_element_located(locator=locator))
            return element
        except (TimeoutException, NoSuchElementException) as err:
            LOGGER.error(err)
            return False

    def elements_are_visible(self, locator, timeout=30):
        try:
            elements = WebDriverWait(driver=self.driver, timeout=timeout).until(

                EC.visibility_of_all_elements_located(locator=locator))
            return elements
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as err:
            LOGGER.error(err)
            return False

    def element_is_present(self, locator, timeout=10):
        try:
            element = WebDriverWait(driver=self.driver, timeout=timeout).until(

                EC.presence_of_element_located(locator=locator))
            return element
        except (TimeoutException, ) as err:
            LOGGER.error(err)
            return False

    def elements_are_present(self, locator, timeout=30):
        try:
            element = WebDriverWait(driver=self.driver, timeout=timeout).until(

                EC.presence_of_all_elements_located(locator=locator))
            return element
        except (TimeoutException, )as err:
            LOGGER.error(err)
            return False

    def element_is_clickable(self, locator, timeout=10):
        try:
            element = WebDriverWait(driver=self.driver, timeout=timeout).until(

                EC.element_to_be_clickable(locator))
            return element
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as err:
            LOGGER.error(err)
            return False

    def element_is_relocated(self, locator):
        while True:
            try:
                element = self.element_is_visible(locator=locator)
                return element
            except StaleElementReferenceException as err:
                LOGGER.error(err)
                return False

    def click_on_button(self, element: WebElement):
        self.driver.execute_script("arguments[0].click()", element)

    def move_to_element(self, argument: WebElement):
        self.driver.execute_script("arguments[0].scrollIntoView();", argument)

    def close_promo_banner(self):
        self.driver.execute_script("document.getElementsByClassName\
        ('promocode-popup__close close-btn')[0].click();")
        return self

    def scroll_down(self, number_px):
        self.driver.execute_script(f"window.scrollTo(0, {number_px});")

    @staticmethod
    def get_attribute_value(element: WebElement, attribute_name: str):
        return element.get_attribute(attribute_name)

    def title_is_present(self, title: str, timeout: int = 30):
        try:
            state = WebDriverWait(self.driver, timeout).until(EC.title_contains(title))
            return state
        except (NoSuchElementException, TimeoutException) as err:
            LOGGER.error(err)
            return False

    def element_is_not_present(self, locator):
        while True:
            try:
                element = self.element_is_present(locator)
                return element
            except StaleElementReferenceException as err:
                LOGGER.error(err)
                print('Element is not attached to page',
                      'Needed to wait',
                      'Trying again', sep='\n')

    def wait_load_page(self):
        try:
            WebDriverWait(self.driver, 10).\
            until(lambda driver: driver.execute_script(
                "return document.readyState === 'complete';"))
            return True
        except TimeoutException as err:
            LOGGER.error(err)
            return False

    def move_to_elem(self, elem: WebElement):
        ActionChains(self.driver).move_to_element(elem).click_and_hold(elem).perform()

    def is_title_present(self):
        return self.driver.title

    def is_new_window_opened(self, handles):
       return WebDriverWait(driver=self.driver, timeout=30).until(EC.new_window_is_opened(handles))

    def dismiss_alert_if_present(self):
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
        except (NoAlertPresentException, TimeoutException) as err:
            LOGGER.error(err)

    def handle_browser_alert(self):
        try:
            alert = WebDriverWait(driver=self.driver, timeout=5).until(EC.alert_is_present())
            alert.dismiss()
            return True
        except TimeoutException as err:
            LOGGER.error(err)
            return False
