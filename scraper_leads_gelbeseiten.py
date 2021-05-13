from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import ActionChains

# Exception handling for radius input range 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import time  # Library to allow waiting and sleep

def scrape_gelbesieten():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.gelbeseiten.de/")


   # Wait for cookie popup to load
    while True:
        try:
            # Accept cookie popup
            cookiesHandle = driver.find_element_by_xpath(
                '//*[@id="cmpwelcomebtnyes"]/a'
            )
            cookiesHandle.click()
            break
        except: 
            time.sleep(1)

    # Fill in search inputs 
    search_input_was = driver.find_element_by_xpath(
        '//*[@id="what_search"]'
    )
    search_input_was.send_keys('steuerberater')

    search_input_wo = driver.find_element_by_xpath(
        '//*[@id="where_search"]'
    )
    search_input_wo.send_keys('berlin')

    send_input_button = driver.find_element_by_xpath(
        '//*[@id="transform_wrapper"]/section/div/div/div/div[1]\
        /div/div/form/div/div[2]/button'
    )
    send_input_button.click()
    
    # Change range to 50 km
    search_radius_range_input = driver.find_element_by_xpath(
        '//*[@id="suchradius_slider"]'
    )

    search_radius_range_input_id = 'suchradius_slider'
    ignored_exceptions = (
        NoSuchElementException,
        StaleElementReferenceException,
    )
    move_radius_range_input = WebDriverWait(
        driver, 
        5,
        ignored_exceptions=ignored_exceptions
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, search_radius_range_input_id)
        )
    )
    move_radius_range_input = ActionChains(driver)
    move_radius_range_input.click_and_hold(
        search_radius_range_input
    ).move_by_offset(250, 0).release().perform()
