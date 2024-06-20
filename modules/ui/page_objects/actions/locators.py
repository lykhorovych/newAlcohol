from selenium.webdriver.common.by import By


class AllActionsLocators:

    # SEARCH PRODUCTS LOCATORS

    DESTINATION_BUTTON = (By.PARTIAL_LINK_TEXT, 'Обрати спосіб доставки')
    CITY_INPUT = (By.CLASS_NAME, 'select2-search__field')
    SELECT_CITY = (By.ID, 'city')
    DELIVERY_BUTTON = (By.ID, 'self-delivery')  
    ADDRESS_FIELD = (By.ID, 'select2-store-address-container')
    SUBMIT_BUTTON = (By.LINK_TEXT, 'Підтвердити')


class EconomyLocators:
    CATALOG_LIST = (By.CSS_SELECTOR, ".catalog-list article")
    PRODUCT_PAGINATIONS_LIST = (By.CLASS_NAME, "product-pagination__item")
    CATEGORY_LIST = (By.CLASS_NAME, "custom-tag__text catalog-subcategory-list__link")
    IMAGE_LINK = (By.XPATH, "/descendant::*[@class='catalog-item__img']")
    PRODUCT_LINK = (By.XPATH, "/descendant::a[@class='catalog-item__photo-link']")
    DESCRIPTION_PRODUCT = (By.XPATH, "//div[contains(@class, 'catalog-item__title')]")
    PRODUCT_PRICE_TOP = (By.XPATH, "/descendant::*[@class='product-price__top']")
    PRODUCT_PRICE_BOTTOM = (By.XPATH, "/descendant::*[@class='product-price__bottom']")
    PRODUCT_ID = (By.CSS_SELECTOR, "custom-tag__text > strong")
    RATING_FIELD = (By.XPATH, "/descendant::div[@class='rating__value']")
    DISCOUNT_FIELD = (By.XPATH, "/descendant::*[@class='custom-product-label']")