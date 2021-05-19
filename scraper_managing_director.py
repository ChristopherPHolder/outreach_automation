import pandas as pd
import numpy as np

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
    driver.implicitly_wait(5)
    df = add_imprint(df, driver)
    driver.close()
    return df

def add_imprint(df, driver):
    n = 0
    for i in df.index:
        if pd.isnull(df['Geschäftsführer'][i]) == True\
        and pd.isnull(df['Web'][i]) == False:
            n += 1
            web_url = df['Web'][i]
            imprint_url = get_imprint_url(web_url, driver)
            df['Impressum'][i] = imprint_url
            print(n, i, df['Web'][i], df['Impressum'][i])
    return df

def check_add_imprint_column(df):
    print(list(df))
    if 'Impressum' not in list(df):
        df['Impressum'] = np.nan
    return df

def get_imprint_url(web_url, driver):
    try:
        driver.get(web_url)
        elems = driver.find_elements_by_xpath("//a[@href]")
    except WebDriverException:
        print('Page down -->', web_url)
        elems = []
    
    for elem in elems:
        try:
            if 'impressum' in elem.get_attribute('href'):
                return elem.get_attribute('href')
        except StaleElementReferenceException:
            pass
    return np.nan
                
# Open file as pd

# Add imprint urls
# Iterate over each lead
    # If lead does not have managing director
    # AND If has website AND no imprint
        # Open website
        # Def get_imprint_url
        # If has imprint
            # Add to pd

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