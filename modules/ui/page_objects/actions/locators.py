from selenium.webdriver.common.by import By


class AllActionsLocators:

    # SEARCH PRODUCTS LOCATORS

    DESTINATION_BUTTON = (BY.LINK_TEXT, 'Обрати спосіб доставки')
    CITY_INPUT = (By.CLASS_NAME, 'select2-search__field')
    SELECT_CITY = (By.ID, 'city')
    DELIVERY_BUTTON = (By.ID, 'self-delivery')  
    ADDRESS_FIELD = (By.ID, 'select2-store-address-container')
    SUBMIT_BUTTON = (By.LINK_TEXT, 'Підтвердити')
