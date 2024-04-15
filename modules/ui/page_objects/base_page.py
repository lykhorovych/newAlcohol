from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchWindowException, TimeoutException,
                                        StaleElementReferenceException, NoSuchElementException, WebDriverException)
from chromedriver_py import binary_path
import undetected_chromedriver as uc
from fake_useragent import UserAgent


class BasePage:

    def __init__(self, browser=None) -> None:
        self.browser = browser
        self.options = webdriver.ChromeOptions()
        self.driver = self.create_new_browser()

    def create_regular_driver(self):
        print("Creating regular driver")
        ua = UserAgent()
        self.options.add_argument("--user-agent=%s" % ua.random)
        self.options.binary_location = r"/usr/bin/google-chrome"
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=self.options)
        driver.maximize_window()
        return driver

    def create_remote_webdriver(self):
        print("Creating remote driver")
        self.options.add_argument("--disable-notifications")
        driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                  options=self.options
                                  )
        return driver

    def create_undetected_driver(self):
        print("Creating undetected driver")
        ua = UserAgent()
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument("--user-agent=%s" % ua.random)
        options.add_argument("--disable-notifications")
        options.add_argument("--headless=new")
        print(binary_path)
        driver = uc.Chrome(
                           driver_executable_path=binary_path,
                           use_subprocess=False,
                           options=options,
                           headless=True
        )
        print(driver.options.binary_location)
        driver.maximize_window()
        return driver

    def create_new_browser(self):
        if self.browser == 'chrome':
            try:
                print("trying to create chrome browser")
                return self.create_regular_driver()
            except (NoSuchWindowException, TimeoutException, StaleElementReferenceException,
                    NoSuchElementException, WebDriverException):
                pass
                # print("trying to create undetected chrome browser")
                # time.sleep(10)
                # return self.create_undetected_driver()
        elif self.browser == 'remote':
            print("trying to create remote browser")
            return self.create_remote_webdriver()
        else:
            print("trying to create undetected chrome browser")
            return self.create_undetected_driver()

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