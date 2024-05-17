from selenium.webdriver.common.by import By


class ATBPageLocators:

    # SEARCH PRODUCTS LOCATORS
    PROMO_POPUP = (By.ID, 'promocodePopup')
    ALCOHOL_MODAL = (By.CSS_SELECTOR, '.alcohol-modal__submit')
    CATALOG_BUTTON = (By.CSS_SELECTOR, "button[aria-controls='catalog-category']")
    CATALOG_LIST = (By.CLASS_NAME, "catalog-button--store")
    ALCOGOL_BUTTON = (By.CLASS_NAME, "home-categories__item--alcohol")
    CATALOG_MENU = (By.CSS_SELECTOR, ".catalog-subcategory-list>span>a")
    ATHER_ALCOGOL_BUTTON = (By.CSS_SELECTOR, "a[href='/catalog/336-inshiy-alkogol'][class*='catalog']")
    LIST_OF_LINKS = (By.CSS_SELECTOR, ".catalog-item--alco .catalog-item__photo .catalog-item__photo-link")
    SUBMIT_BUTTON = (By.CLASS_NAME, "alcohol-modal__submit")

    # CURRENT PRODUCT LOCATORS
    PRODUCT_TITLE = (By.CLASS_NAME, "product-page__title")
    PRODUCT_CODE = (By.CSS_SELECTOR, ".custom-tag__text strong")
    PICTURE_LINK = (By.CSS_SELECTOR, ".cardproduct-tabs__item picture img") #
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-about__price .product-price__top")
    CHARACTERISTICS_VALUES = (By.CSS_SELECTOR,
                              ".product-characteristics__row .product-characteristics__info")


class RozetkaLocators:
    CATALOG_LINK = (By.ID, 'fat-menu')
    ALCO_LINK = (By.XPATH,
                 "//li[@class='menu-categories__item'][14]//a")
    STRONG_DRINKS_LINK = (By.XPATH, "//a[text()='Міцні напої']")
    EXPONEA_BANER = (By.CLASS_NAME, "exponea-banner")
    EXPONEA_BANER_CLOSE_BUTTON = (By.CLASS_NAME, 'exponea-close')
    CHECK_AGE_HEADING = (By.XPATH, "//h2[text()='Підтвердіть свій вік']")
    CHECK_AGE_CLOSE_BUTTON = (By.CSS_SELECTOR, "input[value='Так']")
    ALCO_LINK_2 = (By.CSS_SELECTOR,
                   "a[href*='krepkie-napitki']")
    FILTER_BUTTON = (By.CSS_SELECTOR, 'button[class*="catalog-settings__filter-button"]')
    FREE_DELIVERY_BOX = (By.CSS_SELECTOR, 'a[data-id="Доставка в магазини ROZETKA"]')
    READY_TO_DEPARTURE_BOX = (By.CSS_SELECTOR, 'a[data-id="Готовий до відправлення"]')
    ALCO_TYPES = (By.CSS_SELECTOR, "a.goods-tile__picture")

    # CURRENT PRODUCT LOCATORS
    ALCOHOL_NAME = (By.CSS_SELECTOR, 'h1.product__title-left')
    ALCOHOL_PRICE = (By.CSS_SELECTOR, 'p.product-price__big')
    ALCOHOL_IMAGE_URL = (By.XPATH, '. //li[2]//rz-gallery-main-content-image[1]//img[1]')
    CHARACTERISTIC_VALUES = (By.CLASS_NAME, 'characteristics-full__list')
    ALCOHOL_CODE = (By.XPATH, "//div[@class='product__heading-wrapper']//span[@class='product__code-accent']")
