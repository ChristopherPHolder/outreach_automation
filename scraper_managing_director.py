import pandas as pd
import numpy as np

from tqdm import tqdm

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException,\
                                        StaleElementReferenceException

def add_managing_director(filename):
    df = pd.read_excel("leads/" + filename + ".xlsx")

    df = check_add_imprint_column(df)
    options = Options()    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(2.5)
    df = add_imprint(df, driver)

    df = check_add_imprint_manager_count_column(df)
    df = add_imprint_manager_count(df, df_g, driver)

    driver.close()
    return df

def add_imprint(df, driver):
    n = 0
    with tqdm(
        total = (df.loc[(df['Geschäftsführer'].isnull()) & (df['Impressum'].isnull()), 'Web'].count()),
        desc='Extracting Imprint'
    ) as pbar:

        for i in df.index:
            if pd.isnull(df['Geschäftsführer'][i]) == True\
            and pd.isnull(df['Web'][i]) == False\
            and pd.isnull(df['Impressum'][i]) == True:
                pbar.update(1)
                n += 1
                web_url = df['Web'][i]
                imprint_url = get_imprint_url(web_url, driver)
                df['Impressum'][i] = imprint_url
                
    return df

def check_add_imprint_column(df):
    if 'Impressum' not in list(df):
        df['Impressum'] = np.nan
    return df

def get_imprint_url(web_url, driver):
    try:
        driver.get(web_url)
        elems = driver.find_elements_by_xpath("//a[@href]")
    except WebDriverException:
        elems = []
    
    for elem in elems:
        try:
            if 'impressum' in elem.get_attribute('href'):
                return elem.get_attribute('href')
        except StaleElementReferenceException:
            pass
    return np.nan

def check_add_imprint_manager_count_column(df):
    if 'Impressum Word Count' not in list(df):
        df['Impressum Word Count'] = np.nan
    return df

def add_imprint_manager_count(df, driver):
    manager_titles = get_list_of_manager_titles()
    with tqdm(
        total = df.loc[(df['Geschäftsführer'].isnull()) & (df['Impressum Word Count'].isnull()), 'Impressum'].count(),
        desc='Scraping'
    ) as pbar:

        for i in df.index:
            if  pd.isnull(df['Geschäftsführer'][i]) == True\
            and pd.isnull(df['Impressum'][i]) == False\
            and pd.isnull(df['Impressum Word Count'][i]) == True:
                pbar.update(1)

                imprint_url = df['Impressum'][i]
                
                driver.get(imprint_url)
                for title in manager_titles:
                    elems = driver.find_elements_by_xpath("//*[contains(text(),%s)]" % title)

                    if len(elems) != 0:
                        df['Impressum Word Count'][i] = len(elems)

    return df

def get_list_of_manager_titles():
    df_titles = pd.read_excel("wordlist/manager_titles.xlsx")
    return [df_titles['Manager Title'][i] for i in df_titles.index]

# def add manager names 
# Iterate over each lead
    # If lead does not have managing director
    # AND has imprint
        # Open imprint
        # If 'managing director' (list of words) in imprint
        # def try to parse data to extract names ':)
        # Add name to 'Maybe managing director'

# save file
# close file

# Def get imprint
# Def get mananger name