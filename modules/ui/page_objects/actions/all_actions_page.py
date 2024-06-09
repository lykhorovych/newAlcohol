from selenium.webdriver.support.select import Select

from modules.ui.page_objects.base_page import BasePage
from modules.ui.page_objects.actions.locators import AllActionsLocators



class ATBAllActionsPage(BasePage):
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
