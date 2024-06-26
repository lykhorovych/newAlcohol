from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchWindowException, TimeoutException,
                                        StaleElementReferenceException, NoSuchElementException, WebDriverException)
from selenium.webdriver.common.action_chains import ActionChains
from chromedriver_py import binary_path
import undetected_chromedriver as uc
from fake_useragent import UserAgent


class BasePage:

    def __init__(self, browser=None, headless=None) -> None:
        ua = UserAgent()
        options = uc.ChromeOptions()
        options.add_argument("--user-agent=%s" % ua.random)
        options.binary_location = r"/usr/bin/google-chrome"
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-notifications")
        if headless:
            options.add_argument("--headless=new")
        self.options = options
        self.driver = self.create_new_browser(browser)

    def create_regular_driver(self):
        print("Creating regular driver")
        # browser path for local testing
        # self.options.binary_location = r"/home/olykhorovych/D/courses/project_copy/LykhorovychAlcohol/browser_for_local_testing/chrome-linux/chrome"
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
        print(binary_path)
        driver = uc.Chrome(
                           driver_executable_path=binary_path,
                           use_subprocess=False,
                           options=self.options,
                           #headless=True if headless else False
        )
        print(driver.options.binary_location)
        driver.maximize_window()
        return driver

    def create_new_browser(self, browser):
        if browser == 'chrome':
            try:
                print("trying to create chrome browser_for_local_testing")
                return self.create_regular_driver()
            except (NoSuchWindowException, TimeoutException, StaleElementReferenceException,
                    NoSuchElementException, WebDriverException):
                pass
                # print("trying to create undetected chrome browser_for_local_testing")
                # time.sleep(10)
                # return self.create_undetected_driver()
        elif browser == 'remote':
            print("trying to create remote browser_for_local_testing")
            return self.create_remote_webdriver()
        else:
            print("trying to create undetected chrome browser_for_local_testing")
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


    def move_to_elem(self, elem):
        ActionChains(self.driver).move_to_element(elem).click_and_hold(elem).perform()