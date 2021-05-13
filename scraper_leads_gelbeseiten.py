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
import pandas as pd # Library to store and export data formated as a table

def scrape_gelbesieten():
    print('Starting up scraper')
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
    search_input_was.send_keys('Steuerberater')

    search_input_wo = driver.find_element_by_xpath(
        '//*[@id="where_search"]'
    )
    search_input_wo.send_keys('Munster')

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

    time.sleep(15) # Allows banner add to move out the way

    complete_list_size = driver.find_element_by_xpath(
        '//*[@id="loadMoreGesamtzahl"]'
    ).text
    print('Downloading data from:', complete_list_size, 'leads')
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
            print(current_list_size,end='')
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
    nan = float('NaN')
    
    print('\nProcessing lead data.')
    
    for i in range(int(current_list_size)):
        lead = i + 1
        l = (len(firmenname) - 1)
        print("Lead #", (l+1) , '--', lead)

        move = ActionChains(driver)
        move.move_to_element(
            driver.find_element_by_xpath(
                f'//*[@id="gs_treffer"]/div/article[{lead}]'
            )
        ).perform()
        time.sleep(0.5)

        try:
            companyname = driver.find_element_by_xpath(
                f'//*[@id="gs_treffer"]/div/article[{lead}]/a/h2'
            )
        except:
            print('Error: downloading the lead does not follow the same format')
            continue

        firmenname.append(companyname.text)
        print('Company Name:', firmenname[l])

        geschaftsfuhrer.append(nan)

        address = driver.find_element_by_xpath(
            f'//*[@id="gs_treffer"]/div/article[{lead}]/a/address/p[1]'
        ).text
        
        address_space_split = address.split(' ')

        bezirk = (address_space_split[len(address_space_split) - 3]
        ).replace('(', '').replace(')','')
        bezirk_ort_plz.append(bezirk)
        print('District:', bezirk_ort_plz[l])

        stadt.append(address_space_split[len(address_space_split) - 4])
        print('City:', stadt[l])

        address_coma_split = address.split(',')
        strasse.append(address_coma_split[0])
        print('Street:', strasse[l])

        plz.append(address_coma_split[1])
        print('Postal:', plz[l])


        try:
            tel.append(
                driver.find_element_by_xpath(
                    f'//*[@id="gs_treffer"]/div/article[{lead}]/a/address/p[2]'
                ).text
            )
        except NoSuchElementException:
            tel.append(nan)
        print('Phone:', tel[l])

        try:
            mail_link = driver.find_element_by_xpath(
                f'//*[@id="gs_treffer"]/div/article[{lead}]/div/div/a[2]'
            ).get_attribute('href')
            mail_link_re_split = re.split('\:|\?', mail_link)
            mail.append(mail_link_re_split[1])
        except NoSuchElementException:
            mail.append(nan)
        print('Email:', mail[l])
        try:
            # Check if it said gelbeseite is its site 
            url = (
                driver.find_element_by_xpath(
                    f'//*[@id="gs_treffer"]/div/article[{lead}]/div/div/a[1]'
                ).get_attribute('href')
            )
            url_dot_split = url.split('.')
            if 'gelbeseiten' in url_dot_split:
                url = nan
            
            web.append(url)

        except NoSuchElementException:
            web.append(nan)

        print('Web:', web[l])

    # Creating DataFrame
    lead_data = {
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

    df = pd.DataFrame(data=lead_data)
    pd.set_option('display.max_rows', None)
    print(df)

    driver.close()