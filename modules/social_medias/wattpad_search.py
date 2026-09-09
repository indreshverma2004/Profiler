import time

from colorama import Fore
from selenium import webdriver


def wattpad_module(pren, name):
    print("📔 Searching for Wattpad profiles ...")
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    url = "https://www.wattpad.com/search/{}%20{}/people".format(pren, name)
    try:
        driver.get(url)
        time.sleep(2.0)
        source_code = str(driver.page_source)
        if "Hmmm... il n'y a pas de résultats" in source_code:
            return None
        print(f'   -> {Fore.GREEN}Found !{Fore.RESET} Visit : {url}')
        return url
    except Exception:
        return None
    finally:
        driver.quit()
