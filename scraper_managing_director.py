import pandas as pd
import numpy as np

from tqdm import tqdm

import spacy as spacy

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException,\
                                        StaleElementReferenceException,\
                                        UnexpectedAlertPresentException,\
                                        TimeoutException

def add_managing_director(filename):
    df = pd.read_excel("leads/" + filename + ".xlsx")

    df = check_add_imprint_column(df)
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(2.5)

    df = add_imprint(df, driver)
    save_changes_to_file(df, filename)

    df = check_add_imprint_manager_count_column(df)
    df = add_imprint_manager_count(df, driver)
    save_changes_to_file(df, filename)

    df = add_manager_name(df, driver, filename)
    save_changes_to_file(df, filename)

    driver.close()
    return df

def save_changes_to_file(df, filename):
    df.to_excel("leads/%s.xlsx" % filename, index=False)

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
                df.loc[i, 'Impressum'] = imprint_url
                
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
        except (StaleElementReferenceException, TypeError, UnexpectedAlertPresentException):
            pass
    return False

def check_add_imprint_manager_count_column(df):
    if 'Impressum Word Count' not in list(df):
        df['Impressum Word Count'] = np.nan
    return df

def add_imprint_manager_count(df, driver):
    manager_titles = get_list_of_manager_titles()
    with tqdm(
        total = df.loc[
            (df['Geschäftsführer'].isnull()) & (df['Impressum Word Count'].isnull()) & (df['Impressum'] != False), 'Impressum'
        ].count(),
        desc='Counting Titles'
    ) as pbar:

        for i in df.index:
            if  pd.isnull(df['Geschäftsführer'][i]) == True\
            and pd.isnull(df['Impressum'][i]) == False\
            and df['Impressum'][i] != False\
            and pd.isnull(df['Impressum Word Count'][i]) == True:

                try:                
                    pbar.update(1)
                    try:
                        imprint_url = df['Impressum'][i]
                        if imprint_url != False:
                            print(imprint_url)
                            driver.get(imprint_url)
                    except (TimeoutException, WebDriverException):
                        continue
                    elems = []
                    for title in manager_titles:
                        elem = driver.find_elements_by_xpath("//*[contains(text(),%s)]" % title)
                        if title in elem[0].text:
                            elems.append((elem[0].text).count(title))
                    print(sum(elems))
                    df.loc[i, 'Impressum Word Count'] = sum(elems)
                except UnexpectedAlertPresentException:
                    pass          
    return df

def get_list_of_manager_titles():
    df_titles = pd.read_excel("wordlist/manager_titles.xlsx")
    return [df_titles['Manager Title'][i] for i in df_titles.index]

def extract_manager_name_from_imprint(driver, imprint_url):
    if imprint_url != False:
        try:
            driver.get(imprint_url)
        except (TimeoutException, WebDriverException):
            return np.nan
    
    titles = get_list_of_manager_titles()
    nlp = spacy.load("de_core_news_md")
    for title in titles:
        try:
            elem = driver.find_elements_by_xpath("//*[contains(text(),%s)]" % title)
            i_title = []
            for i in range(len(elem)):
                if title in elem[i].text:
                    i_title.append(i)
            for i in range(len(i_title)):
                doc = nlp(elem[i_title[-i -1]].text)
                for entity in doc.ents:
                    if entity.label_ == 'PER'\
                    and 4 > len((entity.text).split()) > 1:
                        return entity.text
        except StaleElementReferenceException:
            continue
    return np.nan

def add_manager_name(df, driver, filename):
    with tqdm(
        total = df.loc[
            (df['Geschäftsführer'].isnull() == True) & (df['Impressum Word Count'] == 1),
            'Impressum'
        ].count(),
        desc="Extracting names"
    ) as pbar:
        from_save_count = 0
        imprint_url = 'deep-blue.io'
        for i in df.index:
            if pd.isnull(df['Geschäftsführer'][i]) == True\
            and df['Impressum Word Count'][i] == 1\
            and pd.isnull(df['Impressum'][i]) == False:

                if df['Impressum'][i] != imprint_url:
                    imprint_url = df['Impressum'][i]
                    name = extract_manager_name_from_imprint(driver, imprint_url)
                
                df.loc[i, 'Geschäftsführer'] = name
                print(i, 50 - from_save_count, df['Geschäftsführer'][i], imprint_url)
                from_save_count += 1
                pbar.update(1)

            if from_save_count == 50:
                save_changes_to_file(df, filename)
                from_save_count = 0
                
    return df
