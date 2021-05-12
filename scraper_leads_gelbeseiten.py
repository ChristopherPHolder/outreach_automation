from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

import time  # Library to allow waiting and sleep

def scrape_gelbesieten():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.gelbeseiten.de/")

    time.sleep(2)
    return False