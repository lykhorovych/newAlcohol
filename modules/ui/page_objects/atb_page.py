from modules.ui.page_objects.base_page import BasePage
from modules.ui.page_objects.locators import ATBPageLocators
from modules.common.product import Product


class ATBPage(BasePage):
    URL = "https://www.atbmarket.com/"

    def get_primary_alcohol_links(self) -> list:
        self.close_banner(ATBPageLocators.PROMO_POPUP,
                          ATBPageLocators.CLOSE_PROMO_POPUP).\
                          close_banner(ATBPageLocators.ALCOHOL_MODAL,
                                       ATBPageLocators.ALCOHOL_MODAL_SUBMIT)

        self.scroll_down(700)
        alcohol_btn = self.element_is_visible(ATBPageLocators.ALCOGOL_BUTTON)
        if alcohol_btn:
            print("Alcohol button clicked", alcohol_btn)
            self.click_on_button(alcohol_btn)

        self.close_banner(ATBPageLocators.PROMO_POPUP,
                          ATBPageLocators.CLOSE_PROMO_POPUP).\
                          close_banner(ATBPageLocators.ALCOHOL_MODAL,
                                       ATBPageLocators.ALCOHOL_MODAL_SUBMIT)

        ather_alc_btn = self.element_is_visible(ATBPageLocators.ATHER_ALCOGOL_BUTTON)
        if ather_alc_btn:
            print("Ather alcohol button clicked", ather_alc_btn)
            self.click_on_button(ather_alc_btn)

        self.close_banner(ATBPageLocators.PROMO_POPUP,
                          ATBPageLocators.CLOSE_PROMO_POPUP).\
                          close_banner(ATBPageLocators.ALCOHOL_MODAL,
                                       ATBPageLocators.ALCOHOL_MODAL_SUBMIT)

        alco_links = self.elements_are_visible(ATBPageLocators.LIST_OF_LINKS)
        if alco_links:
            print(len(alco_links))
            alco_links = map(lambda x: x.get_attribute("href"), alco_links)
            return alco_links
        return None

    def get_product_characteristics(self):
        title = self.element_is_visible(ATBPageLocators.PRODUCT_TITLE)
        if title:
            title = title.text
        price = self.element_is_visible(ATBPageLocators.PRODUCT_PRICE)
        if price:
            price = float(price.text.split()[0])
        img_link = self.get_attribute_value(self.element_is_visible(ATBPageLocators.PICTURE_LINK),
                                       "src")
        characteristic = self.element_is_visible(ATBPageLocators.CHARACTERISTICS_VALUES)
        if characteristic:
            characteristic = characteristic.text.split("\n")
            characteristic = list(zip(characteristic[::2], characteristic[1::2]))
        alcohol_link = self.driver.current_url
        product_code = self.element_is_present(ATBPageLocators.PRODUCT_CODE)
        if product_code:
            product_code = int(product_code.text)
        is_available = self.element_is_present(ATBPageLocators.AVAILABLE_TEXT)
        if is_available:
            is_available = is_available.text
        product = Product(id=id, name=title, price=price,
                          img=img_link, link=alcohol_link, code=product_code,
                          characteristic=characteristic)

        return product

    def get_properties_of_alcohol_links(self, links: list):
        for id, link in enumerate(links):
            main = self.driver.current_window_handle
            self.switch_to_new_tab(link)
            self.wait_load_page()

            product = self.get_product_characteristics()

            self.driver.close()
            self.driver.switch_to.window(main)
            yield product
