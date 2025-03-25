import os
import subprocess
import logging

from dotenv import load_dotenv
from urllib3.exceptions import NewConnectionError, MaxRetryError
from selenium import  webdriver

from retrying import retry
from django.conf import settings
import undetected_chromedriver as uc
from fake_useragent import UserAgent


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
handler = logging.FileHandler(settings.BASE_DIR / f"data/{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

load_dotenv(settings.BASE_DIR / '.env.scrapping')

data_path = os.getenv("XDG_CACHE_HOME", "/code/data")

state = int(os.getenv('LOCAL', True)) == True
if not state:
    uc.Patcher.data_path = data_path


def get_chrome_driver():
    """get reqular chromedriver"""

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options,
    )
    return driver

def get_firefox_driver():
    """get regular geckodriver"""

    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options,
    )
    return driver

def get_undetected_chrome_driver():
    """get undetected chrome driver"""

    ua = UserAgent()
    options = uc.ChromeOptions()
    options.add_argument(f"--user-agent={ua.random}")
    options.add_argument('--headless=new')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-smooth-scrolling")
    options.add_argument('--disable-dev-shm-usage')

    driver = uc.Chrome(options=options,
    )
    driver.maximize_window()
    return driver

@retry(
        stop_max_attempt_number=3,
        stop_max_delay=10000,
        wait_fixed=1000,
        # retry_on_exception=lambda e: isinstance(e, NewConnectionError) or isinstance(e, ConnectionRefusedError)
    )
def get_undetected_remote_driver():
    """get undetected remote driver"""

    ua = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-agent={ua.random}")
    options.add_argument('--headless=new')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-smooth-scrolling")
    options.add_argument('--disable-gev-shm-usage')
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-features=site-per-process")

    chrome_path = os.getenv("CHROME_BIN_PATH",
        "/usr/src/app/chrome/linux-121.0.6167.85/chrome-linux64/chrome")  # path to browserless:chrome in container

    print("Шлях до undetected_chromedriver:",
        os.path.exists(os.path.join(data_path, 'undetected_chromedriver')))
    print("Шлях до chrome_path:", chrome_path if os.path.exists(chrome_path) else "Not Found")

    driver = uc.Chrome(remote_url=f"{os.getenv('REMOTE_WEBBROWSER', default='http://localhost:3000')}/webdriver",
                        options=options,
                        version_main=121,
                        patch_first=True,
                        data_path=data_path,
                        browser_executable_path=chrome_path if os.path.exists(chrome_path) else None,
    )
    driver.maximize_window()
    return driver

@retry(
    stop_max_attempt_number=3,
    stop_max_delay=10000,
    wait_fixed=1000,
    #    retry_on_exception=lambda e: isinstance(e, NewConnectionError) or isinstance(e, ConnectionRefusedError)
)
def get_remote_webdriver():
    """get remote webdriver"""

    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-smooth-scrolling")
    options.add_argument('--disable-gev-shm-usage')
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-features=site-per-process")

    driver = webdriver.Remote(command_executor=f"{os.getenv('REMOTE_WEBBROWSER', default='http://localhost:3000')}/webdriver",
                              options=options)
    return driver

def get_driver_env():
    return os.getenv("DRIVER_ENV", default="chrome").lower()

def get_driver_by_kind(kind):
    match kind:
        case 'firefox':
            LOGGER.info('you choiced firefox webdriver')
            driver = get_firefox_driver()
        case 'chrome':
            LOGGER.info('you choiced chrome webdriver')
            driver = get_chrome_driver()
        case 'ucd':
            LOGGER.info('you choiced undetected chromedriver')
            driver = get_undetected_chrome_driver()
        case 'urd':
            LOGGER.info('you choiced remote undetected chromedriver')
            driver = get_undetected_remote_driver()
        case 'remote':
            LOGGER.info('you choiced remote webdriver')
            driver = get_remote_webdriver()
        case _:
            raise NotImplementedError("Getting driver for " + kind + " is not implemented yet.")

    return driver

def get_driver():
    return get_driver_by_kind(get_driver_env())
