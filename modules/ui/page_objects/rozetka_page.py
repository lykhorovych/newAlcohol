from modules.ui.page_objects.base_page import BasePage
from modules.ui.page_objects.locators import RozetkaLocators
from modules.common.product import Product
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from modules.common import logger


LOGGER = logger.init_logger(__name__)


class RozetkaPage(BasePage):
    URL = "https://rozetka.com.ua/"

    @staticmethod
    def convert_value(value):
        return "".join(value.split(' '))

    def close_banner(self, *locators):
        try:
            bunner = self.element_is_visible(locators[0])
            if bunner:
                close_button = self.element_is_clickable(locators[1])
                if close_button:
                    try:
                        # scroll to close button
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
                        close_button.click()
                    except ElementClickInterceptedException:
                        try:
                            self.driver.execute_script("arguments[0].click();", close_button)
                        except Exception as js_err:
                            actions = ActionChains(self.driver)
                            actions.move_to_element(close_button)
                            actions.click()
                            actions.perform()
                    print("баннер закрито")
                else:
                    print("кнопка закриття баннера не клікається")
            else:
                print("баннер не знайдено")
        except (NoSuchElementException, TimeoutException) as err:
            print(f"Помилка при закритті баннера {err}")
        return self

    def handle_browser_alert(self):
        try:
            alert = WebDriverWait(driver=self.driver, timeout=5).until(EC.alert_is_present())
            alert.dismiss()
        except TimeoutException as err:
            #LOGGER.error(err)
            print(err)
        return self

    def get_page_title(self, title):
        return self.title_is_present(title)

    def move_to_alco_pages(self):
        if not self.is_title_present() == 'Інтернет-магазин ROZETKA™: офіційний сайт онлайн-гіпермаркету Розетка в Україні':
            raise AssertionError("You dont have access to this page")
        catalog_link = self.element_is_clickable(RozetkaLocators.CATALOG_LINK)
        if catalog_link:
            catalog_link.click()
        self.handle_browser_alert().\
            close_banner(RozetkaLocators.EXPONEA_BANER, RozetkaLocators.EXPONEA_BANER_CLOSE_BUTTON).\
                close_banner(RozetkaLocators.CHECK_AGE_HEADING, RozetkaLocators.CHECK_AGE_CLOSE_BUTTON).\
                close_banner(RozetkaLocators.EXPONEA_FILTER_BANNER, RozetkaLocators.EXPONEA_CLOSE_CROSS_BUTTON)

        # Find and hover over main alcohol link
        main_alco_link = self.element_is_clickable(RozetkaLocators.ALCO_LINK)
        if main_alco_link:
            actions = ActionChains(self.driver)
            actions.move_to_element(main_alco_link).perform() # hover over main alcohol link

            # Find and click the target link
            second_alco_link = self.element_is_clickable(RozetkaLocators.STRONG_DRINKS_LINK)
            if second_alco_link:
                actions.move_to_element(second_alco_link).perform() # hover over target alcohol linkq
                actions.click(second_alco_link).perform()
                #second_alco_link.click()
            else:
                print("target alcohol link not found, trying to open page manually")
                self.driver.get("https://rozetka.com.ua/ua/krepkie-napitki/c4594292/")
        else:
            raise AssertionError("Main alcohol link not found")

        assert self.get_page_title('Міцні напої') is True
        self.handle_browser_alert().\
            close_banner(RozetkaLocators.EXPONEA_BANER, RozetkaLocators.EXPONEA_BANER_CLOSE_BUTTON).\
                close_banner(RozetkaLocators.CHECK_AGE_HEADING, RozetkaLocators.CHECK_AGE_CLOSE_BUTTON).\
                    close_banner(RozetkaLocators.EXPONEA_FILTER_BANNER, RozetkaLocators.EXPONEA_CLOSE_CROSS_BUTTON)

        return True

    def filter_alcohol(self):

        main_url = "https://rozetka.com.ua/ua/krepkie-napitki/c4594292/"
        try:
            alcohol_links = self.elements_are_visible(RozetkaLocators.ALCO_TYPES)
        except Exception as err:
            LOGGER.error(err)
            self.handle_browser_alert().\
                close_banner(RozetkaLocators.EXPONEA_BANER, RozetkaLocators.EXPONEA_BANER_CLOSE_BUTTON).\
                close_banner(RozetkaLocators.CHECK_AGE_HEADING, RozetkaLocators.CHECK_AGE_CLOSE_BUTTON).\
                close_banner(RozetkaLocators.EXPONEA_FILTER_BANNER, RozetkaLocators.EXPONEA_CLOSE_CROSS_BUTTON)
            alcohol_links = self.elements_are_visible(RozetkaLocators.ALCO_TYPES)
        if alcohol_links:
            links = map(
                lambda item: self.get_attribute_value(item, "href"),
                alcohol_links
                )

            yield links  # get all links of alcohol from site

        page = 2

        while True:
            self.driver.get(main_url + f"page={page}/")
            if self.driver.current_url == main_url:
                break
            try:
                alcohol_links = self.elements_are_visible(RozetkaLocators.ALCO_TYPES)
            except Exception as err:
                LOGGER.error(err)
                self.handle_browser_alert().\
                    close_banner(RozetkaLocators.EXPONEA_BANER, RozetkaLocators.EXPONEA_BANER_CLOSE_BUTTON).\
                    close_banner(RozetkaLocators.CHECK_AGE_HEADING, RozetkaLocators.CHECK_AGE_CLOSE_BUTTON).\
                    close_banner(RozetkaLocators.EXPONEA_FILTER_BANNER, RozetkaLocators.EXPONEA_CLOSE_CROSS_BUTTON)
                alcohol_links = self.elements_are_visible(RozetkaLocators.ALCO_TYPES)
            if alcohol_links:
                links = map(
                    lambda item: self.get_attribute_value(item, "href"),
                    alcohol_links)
                print(f"Page {page}")
                yield links  # get all links of alcohol from site
            page += 1

        #return None

    def get_product_data(self):
        title = self.element_is_visible(RozetkaLocators.ALCOHOL_NAME)
        if not (title == False):
            print(title)
            title = title.text
        price = self.element_is_visible(
            RozetkaLocators.ALCOHOL_PRICE)
        if price:
            price = self.convert_value(price.text[:-1])
        img_link = self.element_is_visible(
            RozetkaLocators.ALCOHOL_IMAGE_URL)
        if img_link:
            img_link = self.get_attribute_value(img_link,"src")
        product_link = self.driver.current_url
        product_code = self.element_is_visible(
            RozetkaLocators.ALCOHOL_CODE)
        if product_code:
            product_code = product_code.text.split(" ")[-1]
        characteristic_link = self.element_is_clickable(RozetkaLocators.CHARACTERISTIC_LINK)
        if characteristic_link:
            characteristic_link.click()
        self.wait_load_page()
        try:
            characteristics = self.elements_are_visible(
                RozetkaLocators.CHARACTERISTIC_VALUES)
        except StaleElementReferenceException as err:
            LOGGER.error(err)
            self.handle_browser_alert().\
                close_banner(RozetkaLocators.EXPONEA_BANER, RozetkaLocators.EXPONEA_BANER_CLOSE_BUTTON).\
                    close_banner(RozetkaLocators.CHECK_AGE_HEADING, RozetkaLocators.CHECK_AGE_CLOSE_BUTTON).\
                        close_banner(RozetkaLocators.EXPONEA_FILTER_BANNER, RozetkaLocators.EXPONEA_CLOSE_CROSS_BUTTON)
            characteristics = self.elements_are_visible(
                RozetkaLocators.CHARACTERISTIC_VALUES)
        if characteristics:
            characteristics = map(lambda x: x.text.split("\n"), characteristics)
            characteristic = list(characteristics)
        else:
            characteristic = []
            LOGGER.info(f"Can not find characteristic for those characteristic link\
                {RozetkaLocators.CHARACTERISTIC_LINK} and characteristic values\
                {RozetkaLocators.CHARACTERISTIC_VALUES} locators")
        product = Product(id=id, name=title, price=float(price),
                            img=img_link, link=product_link, code=int(product_code),
                            characteristic=characteristic
                            )
        print(product.to_dict())
        return product

    def get_alcohol(self, links):

        main_window = self.driver.current_window_handle
        for id, link in enumerate(links):
            print(id, link)
            self.switch_to_new_tab(link)
            print(self.driver.current_url)
            #if not self.is_new_window_opened(current_handles):
            #     raise AssertionError("The new alcohol window is not opened")
            self.wait_load_page()
            # close all banners on new page
            self.handle_browser_alert().\
                close_banner(RozetkaLocators.EXPONEA_BANER, RozetkaLocators.EXPONEA_BANER_CLOSE_BUTTON).\
                    close_banner(RozetkaLocators.CHECK_AGE_HEADING, RozetkaLocators.CHECK_AGE_CLOSE_BUTTON).\
                        close_banner(RozetkaLocators.EXPONEA_FILTER_BANNER, RozetkaLocators.EXPONEA_CLOSE_CROSS_BUTTON)

            product = self.get_product_data()
            self.driver.close()
            self.driver.switch_to.window(main_window)

            yield product
