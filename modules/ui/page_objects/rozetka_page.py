from modules.ui.page_objects.base_page import BasePage
from modules.ui.page_objects.locators import RozetkaLocators
from modules.common.product import Product
from selenium.common.exceptions import StaleElementReferenceException


class RozetkaPage(BasePage):
    URL = "https://rozetka.com.ua/ua/"

    @staticmethod
    def convert_value(value):
        return "".join(value.split(' '))


    def close_exponea_banner(self):
        banner = self.element_is_visible(RozetkaLocators.EXPONEA_BANER)
        if banner:
            close_button = self.element_is_clickable(RozetkaLocators.EXPONEA_BANER_CLOSE_BUTTON)
            self.driver.pause(5)
            close_button.click()

    def close_check_age_banner(self):
        banner = self.element_is_visible(RozetkaLocators.CHECK_AGE_HEADING).text
        if banner == 'Підтвердіть свій вік':
            close_button = self.element_is_clickable(RozetkaLocators.CHECK_AGE_CLOSE_BUTTON)
            close_button.click()

    def get_page_title(self, title):
        return self.title_is_present(title)

    def get_alco_links(self):
        main_alco_link = self.element_is_clickable(RozetkaLocators.ALCO_LINK)
        main_alco_link.click()

        assert self.get_page_title('Алкогольні напої і продукти харчування') is True

        self.close_exponea_banner()

        second_alco_link = self.element_is_clickable(RozetkaLocators.ALCO_LINK_2)
        second_alco_link.click()

        assert self.get_page_title('Міцні напої') is True

        self.close_check_age_banner()

        return True

    def filter_alcohol(self):
        self.scroll_down(2400)  # scroll to filter element from begin of site
        filter_delivery = self.element_is_visible(RozetkaLocators.FREE_DELIVERY_BOX)
        filter_delivery_button = self.element_is_clickable(filter_delivery)
        self.click_on_button(filter_delivery_button)

        self.wait_load_page_after_refresh()
        while True:
            try:
                self.element_is_visible(RozetkaLocators.READY_TO_DEPARTURE_BOX)
                break
            except StaleElementReferenceException:
                pass
        ready_to_departure_button = self.element_is_clickable(RozetkaLocators.READY_TO_DEPARTURE_BOX)
        self.click_on_button(ready_to_departure_button)

        self.scroll_down(0)  # scroll to begin of site
        alcohol_links = self.elements_are_visible(RozetkaLocators.ALCO_TYPES)
        if alcohol_links:
            return alcohol_links  # get all links of alcohol from site
        return None

    def get_alcohol(self, links):
        for id, link in enumerate(links):
            main = self.driver.current_window_handle
            alcohol_links = self.elements_are_visible(RozetkaLocators.ALCO_TYPES)
            self.switch_to_new_tab(alcohol_links[id])

            title = self.element_is_visible(RozetkaLocators.ALCOHOL_NAME).text
            price = self.convert_value(self.element_is_visible(
                RozetkaLocators.ALCOHOL_PRICE).text[:-1])
            img_link = self.get_attribute_value(self.element_is_visible(
                RozetkaLocators.ALCOHOL_IMAGE_URL),"src")
            characteristic = self.element_is_visible(
                RozetkaLocators.CHARACTERISTIC_VALUES).text.split("\n")
            product_link = self.driver.current_url
            product_code = self.element_is_visible(
                RozetkaLocators.ALCOHOL_CODE).text.split(" ")[-1]
            characteristic = list(zip(characteristic[::2], characteristic[1::2]))
            product = Product(id=id, name=title, price=float(price),
                              img=img_link, link=product_link, code=int(product_code),
                              characteristic=characteristic
                              )

            self.driver.close()
            self.driver.switch_to.window(main)

            yield product
