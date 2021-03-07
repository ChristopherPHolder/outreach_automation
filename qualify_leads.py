import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlparse
import re
import pandas as pd
from tqdm import tqdm
import numpy as np

from comp.get_user_input import get_wordlist_ql, get_leadsfile_ql

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

    # Total of rows in database
    total_rows = df_web.shape[0]
    counter = 0
    list_of_urls = df_web.Web.tolist()
    totally = []
    totally_content = []
    for url in list_of_urls:
        print("<--------------------------------------------------> ", counter + 1)
        # Extract all links of the page
        try:
            try:
                url = "https://" + url
            except:
                url = "http://" + url
            print("Result for: ", url)
            req = requests.get(url, timeout=5)
            print(req.status_code)
            if req.status_code != 200:
                print("Error obteniendo la página. Status Code", r.status_code)
            soup = BeautifulSoup(req.text, "lxml")
            all_a_s = soup.find_all("a")
        except Exception as e:
            print("Error obtaining page. Exception error:\n", e)
        try:
            list_of_urls_by_page = []
            for item in all_a_s:
                if item is not None:
                    try:
                        list_of_urls_by_page.append(item.get("href"))
                    except:
                        pass
        except:
            pass
        # Filtrate links that contain key words
        try:
            total_sublist = []
            for url_single in list_of_urls_by_page:
                lists = [word for word in subdomains if word.lower() in url_single.lower()]
                if len(lists) >= 1:
                    total_sublist.append(url_single)
        except:
            total_sublist = []
        totally.append(total_sublist)
        counter += 1

        if counter == total_rows:
            break

    list_total = []

    # Initializing new column
    # df_web.loc[:, "qualify"] = np.nan

    # Extract labels for classification
    types = wordlist.State.unique().tolist()
    types.remove("Subdomains")

    index = 0
    ordered = []
    for list_items in totally:
        classifications_of_all_links_in_page = []
        for element in list_items:
            try:
                rr = requests.get(element)
                ss = BeautifulSoup(rr.text, "lxml")
                if ss:
                    print(index + "successful request")
            except Exception as e:
                try:
                    try:
                        new_url = "https://" + df_web.loc[index, "Web"] + element
                    except:
                        new_url = "http://" + df_web.loc[index, "Web"] + element
                    rr = requests.get(new_url)
                    ss = BeautifulSoup(rr.text, "lxml")
                except:
                    ss = ""
            classification = []
            for tp in types:
                list_of_words_to_match = wordlist[wordlist["State"] == tp].Word.tolist()
                words_founded = [
                    word
                    for word in list_of_words_to_match
                    if word.lower() in str(ss).lower()
                ]
                if len(words_founded) >= 1:
                    classification.append(tp)
            classifications_of_all_links_in_page.append(classification)
        ordered.append(classifications_of_all_links_in_page)
        index += 1


    def priorities(list_of_items):
        qualifying = []
        for items in list_of_items:
            total_links = []
            for item in items:
                total_links.append(len(item))
                if (("No" in item) and ("Fuck Yes" in item) and ("Yes" in item)) or (("No" in item) and ("Fuck Yes" in item)) or (("No" in item) and ("Yes" in item)):
                    status = "No"
                elif (
                    ("No" in item)
                    and ("Fuck Yes" in item)
                    and ("Yes" in item)
                    and ("Maybe" in item)
                ):
                    status = "Maybe"
                elif ("No" in item) and ("Maybe" in item):
                    status = 'Maybe'
                else:
                    for tt in item:
                        status = tt
            if sum(total_links) == 0:
                status = "Fuck No"
            qualifying.append(status)
        return qualifying

    def set_value(row_number, assigned_value): 
        return assigned_value[row_number] 

    assigning = { "Fuck No": 1,"No": 3, "Maybe": 4, "Yes": 5, "Fuck Yes": 6 }
    
    qualifier = pd.Series(priorities(ordered)).apply(set_value, args =(assigning, ))
    df_web.insert(loc = 0, column = 'Qualifier', value = qualifier)
    df_no_web.insert(loc = 0, column = 'Qualifier', value = 0)

    df_no_web.insert(loc = 1, column = 'Tag', value = 'no web')
    assigning_tag = { 0: "NoWeb", 1: "NoCarrierF", 2: "NoHire", 3: "NotNow", 4: "MaybeHire", 5: "YesHire", 6: "HireNow" }
    tags = df_web['Qualifier'].apply(set_value, args =(assigning_tag, ))
    df_web.insert(loc = 1, column = 'Tag', value = tags)

    df_t = df_web.append(df_no_web, ignore_index=True, sort=False)

    filename = filename + "_qualified"
    df_t.to_excel("leads/" + filename + ".xlsx")

    return filename

wordlist = get_wordlist_ql()
filename = get_leadsfile_ql()
qualify_leads_fn(filename, wordlist)