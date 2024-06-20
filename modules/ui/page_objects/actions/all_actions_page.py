from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

from modules.ui.page_objects.base_page import BasePage
from modules.ui.page_objects.actions.locators import AllActionsLocators, EconomyLocators
from modules.ui.page_objects.locators import ATBPageLocators


class ATBAllActionsPage(BasePage):
    
    CATALOG_LIST = (By.CSS_SELECTOR, ".catalog-list article")
    PRODUCT_PAGINATIONS_LIST = (By.XPATH,
                                 "//*[@class='product-pagination__item']")
    CATEGORY_LIST = (By.CLASS_NAME,
                      "custom-tag__text catalog-subcategory-list__link")
    IMAGE_LINK = (By.XPATH,
                   "(//*[@class='catalog-item__img'])")
    PRODUCT_LINK = (By.XPATH,
                     "(//a[@class='catalog-item__photo-link'])")
    DESCRIPTION_PRODUCT = (By.XPATH,
                            "(//*[contains(@class, 'catalog-item__title')])")
    PRODUCT_PRICE_TOP = (By.XPATH,
                          "(//div[contains(@class, 'product-price--weight')]//data[@class='product-price__top' and not(@value='')])")
    PRODUCT_PRICE_BOTTOM = (By.XPATH, 
                            "(//div[contains(@class, 'product-price--weight')]//data[@class='product-price__bottom' and not(@value='')])")
    PRODUCT_ID = (By.CSS_SELECTOR,
                   "custom-tag__text > strong")
    RATING_FIELD = (By.XPATH,
                     "(//div[@class='rating__value'])")
    DISCOUNT_FIELD = (By.XPATH,
                       "(//*[@class='custom-product-label' and not(@style)])")
    ARTICLE = (By.XPATH, "(//article[contains(@class, 'catalog-item')])")

    
    URL = "https://www.atbmarket.com/promo/all/"

    def get_current_address_shop(self, city: str):

        select_city_button = self.element_is_clickable(AllActionsLocators.DESTINATION_BUTTON)
        if select_city_button.is_clickable():
            select_city_button.click()

        select_city_field = Select(self.element_is_visible(AllActionsLocators.SELECT_CITY))
        select_city_field.select_by_visible_text(city.title())
        selected_field = select_city_field.first_selected_option.text

        delivery_button = self.element_is_clickable(AllActionsLocators.DELIVERY_BUTTON)
        delivery_button.click()  

        address_field = self.element_is_visible(AllActionsLocators.ADDRESS_FIELD).text
        if address_field == 'вул. Золота, 7':
            submit_button = self.element_is_clickable(AllActionsLocators.SUBMIT_BUTTON)
            data = self.get_attribute_value(submit_button ,'data-req')
            if data['city-id'] == '959':
                submit_button.click()
        
        return True


    def get_all_pages(self):
        pages = self.elements_are_visible(EconomyLocators.PRODUCT_PAGINATIONS_LIST)
        
        return pages
    

    def get_category_list(self):
        categories = self.elements_are_visible(EconomyLocators.CATEGORY_LIST)

        return categories


    def get_page_products(self):
        products = self.elements_are_visible(EconomyLocators.CATALOG_LIST)
        
        return products


    def get_product_link(self, i=1):
        selector, locator = self.PRODUCT_LINK
        product_link = self.element_is_visible((selector, locator + f"[{i}]"))

        return self.get_attribute_value(product_link, "href")


    def get_rating(self, i=1):
        selector, locator = self.RATING_FIELD
        rating = self.element_is_visible((selector, locator + f"[{i}]"))

        return int(rating.text)
    

    def get_discount(self, i=1):
        selector, locator = self.DISCOUNT_FIELD
        discount = self.element_is_visible((selector, locator + f"[{i}]")).text

        return int(discount.strip()[1:-1])
    

    def get_product_description(self, i=1):
        selector, locator = self.DESCRIPTION_PRODUCT
        desc = self.element_is_visible((selector, locator + f"[{i}]"))

        return desc.text
    

    def get_product_price_top(self, i=1):
        selector, locator = self.PRODUCT_PRICE_TOP
        
        price = self.element_is_visible((selector, locator + f"[{i}]"))
        
        return float(self.get_attribute_value(price, 'value'))
    

    def get_product_price_bottom(self, i=1):
        selector, locator = self.PRODUCT_PRICE_BOTTOM
        
        price = self.element_is_visible((selector, locator + f"[{i}]"))
        
        return float(self.get_attribute_value(price, 'value'))
        

    def get_image_link(self, i=1):
        selector, locator = self.IMAGE_LINK
        img = self.element_is_visible((selector, locator + f"[{i}]"))

        return self.get_attribute_value(img, 'src')


    def get_product_id(self) -> int:
        product_id = self.element_is_present(EconomyLocators.PRODUCT_ID)

        return int(product_id.text)


    def get_article_classes(self, i=1):
        selector, locator = self.ARTICLE
        article = self.element_is_present((selector, locator + f"[{i}]"))

        return self.get_attribute_value(article, "class")


    def close_alco_banner(self):
        alcohol_banner = self.element_is_visible(ATBPageLocators.ALCOHOL_MODAL)
        if alcohol_banner:
            alcohol_banner.click()

    