import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlparse
import re
import pandas as pd
from tqdm import tqdm
import numpy as np

from comp.get_user_input import get_wordlist_ql, get_leadsfile_ql


from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



def qualify_leads_fn(filename, wordlist):

    # Open leadsfile
    df = pd.read_excel("leads/" + filename + ".xlsx")

    # Drop extra column
    try:
        df.drop('Unnamed: 0', axis=1, inplace=True)
    except:
        pass

    # Filtering companies with web
    df_web = df[pd.notnull(df["Web"])].reset_index(drop=True)
    df_no_web = df[pd.isnull(df["Web"])].reset_index(drop=True)

    # Extract subdomains to make the first filter
    subdomains = wordlist[wordlist["State"] == "Subdomains"].Word.tolist()

    options = Options()
    options.add_argument("--lang=en")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    # Total of rows in database
    total_rows = df_web.shape[0]
    counter = 0
    list_of_urls = df_web.Web.tolist()
    totally = []
    totally_content = []
    urls_with_subdomain = []
    for url in list_of_urls:
        print("<--------------------------------------------------> ", counter + 1)
        # Extract all links of the page
        try:
            try:
                print("Result for: ", url)
                url = "https://" + url
                driver.get(url)
                print('was with https')
            except:
                url = "http://" + url
                driver.get(url)
                print("Result for: ", url)
                print('was with http')
        except Exception as e:
            print("Error obtaining page. Exception error:\n", e)

        elems = driver.find_elements_by_xpath("//a[@href]")
        list_of_urls_by_page = [elem.get_attribute("href") for elem in elems]
        try:
            total_sublist = []
            for url_single in list_of_urls_by_page:
                lists = [word for word in subdomains if word.lower() in url_single.lower()]
                if len(lists) >= 1:
                    total_sublist.append(url_single)
        except:
            total_sublist = []
        totally.append(total_sublist)
        urls_with_subdomain.append(list(set(total_sublist)))
        counter += 1

        if counter == total_rows:
            break

    types = wordlist.State.unique().tolist()
    types.remove("Subdomains")

    index = 0
    ordered = []
    for list_items in totally:
        print("<--------------------------------------------------> ", index + 1)
        print(df_web.loc[index, "Firmenname"])
        classifications_of_all_links_in_page = []
        for element in list_items:
            try:
                driver.get(element)
                ss = driver.page_source
                text_found = re.search(r'text_to_search', ss)
                if text_found:
                    print(index + "successful request .. len: ", len(text_found))
            except Exception as e:
                try:
                    try:
                        new_url = "https://" + df_web.loc[index, "Web"] + element
                        driver.get(new_url)
                        ss = driver.page_source
                    except:
                        new_url = "http://" + df_web.loc[index, "Web"] + element
                        driver.get(new_url)
                        ss = driver.page_source
                    print(type(ss))
                except:
                    ss = ""
            classification = []
            for tp in types:
                list_of_words_to_match = wordlist[wordlist["State"] == tp].Word.tolist()
                words_founded = [word for word in list_of_words_to_match if word.lower() in ss.lower()]
                if len(words_founded) >= 1:
                    classification.append(tp)
            classifications_of_all_links_in_page.append(classification)
        adding = [item for elem in classifications_of_all_links_in_page for item in elem]
        print(adding)
        ordered.append(adding)
        index += 1

    driver.close()

    def priorities(list_of_items):
        qualifying = []
        for items in list_of_items:
            if (("NoHire" in items) and ("HireNow" in items) and ("YesHire" in items)) or (("NoHire" in items) and ("HireNow" in items)) or (("NoHire" in items) and ("YesHire" in items)):
                status = "NoHire"
            elif ("MaybeHire" in items) and ("HireNow" in items) and ("YesHire" in items) and len(list(set(items)))==3:
                status = "HireNow"
            elif ("YesHire" in items) and ("MaybeHire" in items) and len(list(set(items)))==2:
                status = 'YesHire'
            elif ("YesHire" in items) and ("HireNow" in items) and len(list(set(items)))==2:
                status = 'HireNow'
            elif len(items)>=1:
                status = items[0]
            if len(items) == 0:
                status = "NoCarrierF"
            qualifying.append(status)
        return qualifying

    def set_value(row_number, assigned_value): 
        return assigned_value[row_number]

    assigning = { "NoWeb":0, "NoCarrierF":1, "NoHire":2, "NotNow":3, "MaybeHire":4, "YesHire":5, "HireNow":6 }

    classification_priorities = priorities(ordered)
    
    qualifier = pd.Series(classification_priorities).apply(set_value, args =(assigning, ))

    df_no_web.insert(loc = 0, column = 'Tag', value = 'NoWeb')
    df_web.insert(loc = 0, column = 'Tag', value = classification_priorities)

    df_web.insert(loc = 0, column = 'Qualifier', value = qualifier)
    df_no_web.insert(loc = 0, column = 'Qualifier', value = 0)

    df_web.insert(loc= 2, column='URL', value = urls_with_subdomain)
    df_no_web.insert(loc= 2, column='URL', value = '')

    df_t = df_web.append(df_no_web, ignore_index=True, sort=False)

    filename = filename + "_qualified"
    df_t.to_excel("leads/" + filename + ".xlsx")

    return filename