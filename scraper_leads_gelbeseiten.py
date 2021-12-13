from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
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
from tqdm import tqdm  # Progress bar / counter
import numpy as np # Numerical (np.nan)

def scrape_gelbesieten(company_type, location):

    search_url = (
        'https://www.gelbeseiten.de/Suche/%s/%s' % (
            company_type, location
        )
    )

    options = Options()
    options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(search_url)

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
    """
    # Fill in search inputs
    search_input_was = driver.find_element_by_xpath(
        '//*[@id="what_search"]'
    )
    search_input_was.send_keys(company_type)

    search_input_wo = driver.find_element_by_xpath(
        '//*[@id="where_search"]'
    )
    search_input_wo.send_keys(location)

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

    try:
        # Get complete list of leads in the location
        initial_list_size = driver.find_element_by_xpath(
            '//*[@id="loadMoreGezeigteAnzahl"]'
        ).text
        initial_time = time.perf_counter()
    except NoSuchElementException:
        return pd.DataFrame()
    
    for i in tqdm(range(300), desc='Pre-loading'):
        time.sleep(0.05) # Allows banner add to move out the way
    """

    initial_time = time.perf_counter()

    complete_list_size = driver.find_element_by_xpath(
        '//*[@id="mod-TrefferlisteInfo"]'
    ).text

    current_list_size = complete_list_size
    initial_list_size = 50
    
    with tqdm(
        total=int(complete_list_size), 
        initial=50, desc='Downloading') as pbar:
        downloading = True
        while downloading:
            try:
                current_list_size = driver.find_element_by_xpath(
                    '//*[@id="loadMoreGezeigteAnzahl"]'
                ).text
                if current_list_size == initial_list_size:
                    if (time.perf_counter() - initial_time) > 30:
                        print('Error: page took longer then 30 sec \
                            to load next set of content')
                        pass
                        #return pd.DataFrame()
                else:
                    pbar.update(int(current_list_size) - int(initial_list_size))
                    initial_list_size = current_list_size

                try:
                    time.sleep(0.5)
                    button_mehr_anzeigen = driver.find_element_by_xpath(
                        '//*[@id="mod-LoadMore--button"]'
                    )
                    button_mehr_anzeigen.click()
                    time.sleep(0.5)
                except ElementNotInteractableException as e:
                    print(e)
            except NoSuchElementException as e:
                print(e)
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
    
    for i in tqdm(range(int(current_list_size)), desc='Processing '):
        lead = i + 1
        l = (len(firmenname) - 1)

        try:
            companyname = driver.find_element_by_xpath(
                f'//*[@id="gs_treffer"]/div/article[{lead}]/a/h2'
            )
        except:
            continue

        firmenname.append(companyname.text)

        geschaftsfuhrer.append(np.nan)

        try:
            address = driver.find_element_by_xpath(
                f'//*[@id="gs_treffer"]/div/article[{lead}]/a/address/p[1]'
            ).text

            address_dict = parse_address(address)
            
            try:
                bezirk_ort_plz.append(address_dict['Bezirk'])
            except KeyError:
                bezirk_ort_plz.append(np.nan)

            try:
                strasse.append(address_dict['Strasse'])
            except KeyError:
                strasse.append(np.nan)

            try:
                plz.append(address_dict['Plz'])
            except KeyError:
                plz.append(np.nan)

            try:
                stadt.append(address_dict['Stadt'])
            except KeyError:
                stadt.append(np.nan)

        except NoSuchElementException:
            bezirk_ort_plz.append(np.nan)
            strasse.append(np.nan)
            plz.append(np.nan)
            stadt.append(np.nan)


        try:
            tel.append(
                driver.find_element_by_xpath(
                    f'//*[@id="gs_treffer"]/div/article[{lead}]/a/address/p[2]'
                ).text
            )
        except NoSuchElementException:
            tel.append(np.nan)

        try:
            mail_link = driver.find_element_by_xpath(
                f'//*[@id="gs_treffer"]/div/article[{lead}]/div/div/a[2]'
            ).get_attribute('href')

            mail_dot_split = mail_link.split('.')
            if 'gelbeseiten' in mail_dot_split:
                mail.append(np.nan)
            else: 
                mail_link_re_split = re.split('\:|\?', mail_link)
                mail.append(mail_link_re_split[1])
        except NoSuchElementException:
            mail.append(np.nan)

        try:
            # Check if it said gelbeseite is its site 
            url = (
                driver.find_element_by_xpath(
                    f'//*[@id="gs_treffer"]/div/article[{lead}]/div/div/a[1]'
                ).get_attribute('href')
            )
            url_dot_split = url.split('.')
            if 'gelbeseiten' in url_dot_split or '@' in url:
                url = np.nan

            web.append(url)

        except NoSuchElementException:
            web.append(np.nan)


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
    driver.close()
    return df

def parse_address(address):

    address_dict = {}
    try: 
        # Remove doble comas
        address.replace(',,', ',')
        
        # Extract strasse
        address_coma_split = address.split(',')
        address_dict['Strasse'] = address_coma_split[0]

        # Extract plz
        address_coma_split_1 = address_coma_split[1]
        address_coma_split_1_space_split = address_coma_split_1.split(' ')
        try:
            address_coma_split_1_space_split.remove('')
        except ValueError:
            pass
        if address_coma_split_1_space_split[0].isnumeric()\
            and len(address_coma_split_1_space_split[0]) == 5:
            address_dict['Plz'] =  address_coma_split_1_space_split[0]
            address_coma_split_1_space_split.remove(address_coma_split_1_space_split[0])
        else:
            address_dict['Plz'] = np.nan

        # Extract stadt
        stadt_dict = np.nan

        for i in range(len(address_coma_split_1_space_split)):
            if i == 0:
                if address_coma_split_1_space_split[0].isnumeric() == False:
                    stadt_dict = address_coma_split_1_space_split[0]
                    address_coma_split_1_space_split.remove(address_coma_split_1_space_split[0])
            elif i != 0:
                if address_coma_split_1_space_split[0].isnumeric() == False \
                and '(' not in address_coma_split_1_space_split[0]:
                    stadt_dict += ' ' + address_coma_split_1_space_split[0]
                    address_coma_split_1_space_split.remove(address_coma_split_1_space_split[0])

                address_dict['Stadt'] = stadt_dict
                
            else:
                address_dict['Stadt'] = np.nan

        try:
            if address_coma_split_1_space_split[0].isnumeric() == False:
                address_dict['Bezirk'] = address_coma_split_1_space_split[0].replace('(', '').replace(')', '')
            else:
                address_dict['Bezirk'] = np.nan 
        except IndexError:
                address_dict['Bezirk'] = np.nan
    except IndexError:
        address_dict['Strasse'] = np.nan
        address_dict['Stadt'] = np.nan
        address_dict['Bezirk'] = np.nan
        address_dict['Plz'] = np.nan
        
    return address_dict