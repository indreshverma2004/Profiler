import time

from colorama import Fore
from selenium import webdriver


def webdriver_usage(name, pren):
    print("🎧 Searching for soundcloud profiles ...")
    try:
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        try:
            driver.get(f"https://soundcloud.com/search/people?q={pren} {name}")
            time.sleep(4.0)
            source_code = str(driver.page_source)
            if "Check the spelling, or try a different search." in source_code or "Sorry we didn't find any results for" in source_code:
                return None
            print(f'   -> {Fore.GREEN}Found !{Fore.RESET} Visit : https://soundcloud.com/search/people?q={pren}%20{name}')
            return f'https://soundcloud.com/search/people?q={pren}%20{name}'
        finally:
            driver.quit()
    except Exception:
        return None
