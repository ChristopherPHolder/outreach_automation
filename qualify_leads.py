import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np

# Importing keywords
wordlist = pd.read_excel("wordlist.xlsx")

# Importing data with urls
df = pd.read_excel("steuerberater_kärnten.xlsx")

# Filtering companies with web
df_web = df[pd.notnull(df["Web"])].reset_index(drop=True)

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
        url = "https://" + url
        print("result for: ", url)
        req = requests.get(url, timeout=5)
        print(req.status_code)
        if req.status_code != 200:
            print("Error obteniendo la página. Status Code", r.status_code)
        soup = BeautifulSoup(req.text, "lxml")
        all_a_s = soup.find_all("a")
    except Exception as e:
        print("Error obtaining page. Exception ", e)
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
df_web.loc[:, "qualify"] = np.nan

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
                print("successful request")
        except Exception as e:
            try:
                new_url = "https://" + df_web.loc[index, "Web"] + element
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


df_web.loc[:, "qualify"] = priorities(ordered)
df_web.to_excel("qualifier_file.xlsx")