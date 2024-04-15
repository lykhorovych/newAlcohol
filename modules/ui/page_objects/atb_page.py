from modules.ui.page_objects.base_page import BasePage
from modules.ui.page_objects.locators import ATBPageLocators
from modules.common.product import Product


class ATBPage(BasePage):
    URL = "https://www.atbmarket.com/"

    def get_primary_alcohol_links(self) -> list:

        promo_banner = self.element_is_visible(ATBPageLocators.PROMO_POPUP)
        if promo_banner:  # to close promo banner if it is present
            self.close_promo_banner()

        alcohol_banner = self.element_is_visible(ATBPageLocators.ALCOHOL_MODAL)
        if alcohol_banner:
            alcohol_banner.click()

        self.scroll_down(700)
        alcohol_btn = self.element_is_visible(ATBPageLocators.ALCOGOL_BUTTON)
        self.click_on_button(alcohol_btn)

        alcohol_banner = self.element_is_visible(ATBPageLocators.ALCOHOL_MODAL)
        if alcohol_banner:
            alcohol_banner.click()

        ather_alc_btn = self.element_is_visible(ATBPageLocators.ATHER_ALCOGOL_BUTTON)
        self.click_on_button(ather_alc_btn)

        alcohol_banner = self.element_is_visible(ATBPageLocators.ALCOHOL_MODAL)
        if alcohol_banner:
            alcohol_banner.click()

        alco_links = self.elements_are_visible(ATBPageLocators.LIST_OF_LINKS)
        return alco_links

    def get_properties_of_alcohol_links(self, links: list):
        for id, link in enumerate(links):
            main = self.driver.current_window_handle
            alco_links = self.elements_are_visible(ATBPageLocators.LIST_OF_LINKS)
            self.switch_to_new_tab(alco_links[id])

            title = self.element_is_visible(ATBPageLocators.PRODUCT_TITLE).text
            price = self.element_is_visible(ATBPageLocators.PRODUCT_PRICE).text.split()[0]
            img_link = self.get_attribute_value(self.element_is_visible(ATBPageLocators.PICTURE_LINK),
                                           "src")
            characteristic = self.element_is_visible(ATBPageLocators.CHARACTERISTICS_VALUES).text.split("\n")
            alcohol_link = self.driver.current_url
            product_code = self.element_is_present(ATBPageLocators.PRODUCT_CODE).text
            characteristic = list(zip(characteristic[::2], characteristic[1::2]))
            product = Product(id=id, name=title, price=float(price),
                              img=img_link, link=alcohol_link, code=int(product_code),
                              characteristic=characteristic)

            self.driver.close()
            self.driver.switch_to.window(main)
            yield product



