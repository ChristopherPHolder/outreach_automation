from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import ActionChains

# Exception handling for radius input range 
from selenium.common.exceptions import NoSuchElementException, \
    StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import time  # Library to allow waiting and sleep
import re # Library for resplting data

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
            time.sleep(2)

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

    # Get complete list of leads in the location
    initial_list_size = driver.find_element_by_xpath(
        '//*[@id="loadMoreGezeigteAnzahl"]'
    ).text
    initial_time = time.perf_counter()
    while True:
        current_list_size = driver.find_element_by_xpath(
            '//*[@id="loadMoreGezeigteAnzahl"]'
        ).text
        if current_list_size == initial_list_size:
            if (time.perf_counter() - initial_time) > 300:
                print('Error: page took longer then 5 min \
                    to load next set of content')
                exit()
        else:
            initial_list_size = current_list_size
        try:
            button_mehr_anzeigen = driver.find_element_by_xpath(
                '//*[@id="mod-LoadMore--button"]'
            )
            button_mehr_anzeigen.click()
            time.sleep(2)
        except ElementNotInteractableException:
            break

    # Initializing list
    geschaftsfuhrer = []
    bezirk_ort_plz = []
    firmenname = []
    strasse = []
    plz = []
    stadt = []
    tel = []
    mail = []
    web = []

    for lead in range(current_list_size):
        geschaftsfuhrer.append(NaN = float('NaN'))
        
        address = driver.find_element_by_xpath(
            f'//*[@id="gs_treffer"]/div/article[{lead}]/a/address/p[1]'
        ).text
        address_split = re.split(',|\(|\)', address)
        address_re_split = address_split[1].split(' ')

        bezirk_ort_plz.append(address_split[2])

        firmenname.append(
            driver.find_element_by_xpath(
                f'//*[@id="gs_treffer"]/div/article[{lead}]/a/h2'
            ).text
        )

        strasse.append(address_split[0])

        plz.append(address_re_split[1])

        stadt.append(address_re_split[2])

        tel.append(
            driver.find_element_by_xpath(
                f'//*[@id="gs_treffer"]/div/article[{lead}]/a/address/p[2]'
            ).text
        )

        mail_link = driver.find_element_by_xpath(
            f'//*[@id="gs_treffer"]/div/article[{lead}]/div/div/a[2]'
        ).get_attribute('href')
        mail_link_re_split = re.split('\:|\?', mail_link)
        mail.append(mail_link_re_split[1])

        web.append(
            driver.find_element_by_xpath(
                f'//*[@id="gs_treffer"]/div/article[{lead}]/div/div/a[1]'
            ).get_attribute('href')
        )

    # Creating DataFrame
    lead_info = {
        'Geschäftsführer': geschaftsfuhrer, 
        'Bezirk/Ort/Plz': bezirk_ort_plz, 
        'Firmenname': firmenname, 
        'Straße': strasse,
        'PLZ': plz, 
        'Stadt': stadt,
        'Tel': tel, 
        'Mail': mail, 
        'Web': web,
    }