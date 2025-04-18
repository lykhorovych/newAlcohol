import os.path
import json
import requests

from selenium.common.exceptions import NoSuchWindowException, TimeoutException, JavascriptException
from urllib3.exceptions import MaxRetryError, NewConnectionError
from modules.ui.page_objects.atb_page import ATBPage
from modules.ui.page_objects.rozetka_page import RozetkaPage
from modules.common.product import Product
from modules.common.parsers.parser import args
from config.config import BASE_DIR


def get_list_of_alcohols():
    page = ATBPage()
    page.open(url=page.URL)

    try:
        for alcohol in page.get_properties_of_alcohol_links(page.get_primary_alcohol_links()):
            yield alcohol
    except (NoSuchWindowException, TimeoutException):
        page.driver.save_screenshot(
            BASE_DIR / 'screenshots/screenshot_selenium_error.png'
        )
    except JavascriptException:
        page.driver.save_screenshot(
            BASE_DIR / 'screenshots/screenshot_javascript_error.png'
        )
    except requests.exceptions.ConnectionError:
        page.driver.save_screenshot(
            BASE_DIR / 'screenshots/screenshot_connection_error.png'
        )
    except (MaxRetryError, NewConnectionError):
        pass
    finally:
        page.close()


def get_list_of_alcohol_in_rozetka():
    page = RozetkaPage()
    print(page.URL)
    page.open(page.URL)
    # page.switch_to_handle()

    try:
        if page.move_to_alco_pages():
            #for product in page.get_alcohol(page.filter_alcohol()):
            #    yield product
            # get generator of alcohol pages
            alcohol_pages = page.filter_alcohol() # return a generator of lists
            # get generator of products from each alcohol page
            for page_links in alcohol_pages:  # page_links - it is list of links
                #products = page.get_alcohol(page_links)  # return a generator of products
                #for product in products:
                #    yield product
                yield from page.get_alcohol(page_links)
    except (NoSuchWindowException, TimeoutException):
        page.driver.save_screenshot(
            BASE_DIR / 'screenshots/screenshot_selenium_error.png'
        )
    except JavascriptException:
        page.driver.save_screenshot(
            BASE_DIR / 'screenshots/screenshot_javascript_error.png'
        )
    except requests.exceptions.ConnectionError:
        page.driver.save_screenshot(
            BASE_DIR / 'screenshots/screenshot_connection_error.png'
        )
    except (MaxRetryError, NewConnectionError):
        pass
    finally:
        page.close()


def dump_alcohol(alcohol: Product, filename: str):
    if not os.path.exists(os.path.join(BASE_DIR, filename)):
        with open(BASE_DIR / filename, 'w') as file:
            json.dump([], file, indent=4)
    with open(BASE_DIR / filename, 'r+') as file:
        l = json.load(file)
        l.append(alcohol)
        file.seek(0)
        json.dump(l, file, indent=4, default=Product.to_dict)


def load_all_alcohols(filename: str):
    with open(BASE_DIR / filename, 'r') as file:
        readed_alcohols = json.load(file)
        for alcohol in readed_alcohols:
            yield alcohol


if __name__ == '__main__':

    alcohol_atb = get_list_of_alcohols()
    for alcohol in alcohol_atb:
        dump_alcohol(alcohol, 'alcohols_atb.json')
    alcohol_rozetka = get_list_of_alcohol_in_rozetka()
    for alcohol in alcohol_rozetka:
        dump_alcohol(alcohol, 'alcohols_rozetka.json')
