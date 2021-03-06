import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlparse
import re
import pandas as pd
from tqdm import tqdm

# Importing wordlist
def get_wordlist_ql():
    wordlistfile = input("Insert wordlist: ")
    if wordlistfile == "":
        print("The default wordlist used")
        wordlistfile = "wordlist.xlsx"
    try: 
        wordlist = pd.read_excel(wordlistfile)
        print("Succesfully imported wordlist from: " + wordlistfile)
        return wordlist

    except FileNotFoundError:
        print("\nError: Wordlist file not found!")
        print("Check if you did any typos and that the file is in the correct folder.\
            \nOnce you found the error, try to run the program again.\
            \nRemeber you can leave the field blank and it will use wordlist.xlsx \n")
        quit()

# Import leads data
def get_leadsfile_ql():
    leadsfile = input("\nInsert leads: ")
    
    # Import generic file for testing
    if leadsfile == "t":
        print("The the testing leads file was used.")
        leadsfile = "steuerberater_kärnten_test.xlsx"
    try:
        df = pd.read_excel(leadsfile)
        print("Succesfully imported leads from: " + leadsfile)
        return df

    except FileNotFoundError:
        print("\nError: leads file not found!\
            \n Check if you did any typos and that the file is in the correct folder\
            \nOnce you found the error, try to run the program again.")
        quit()

    except AssertionError:
        print("\nA leads file is necesarry for this program. No file name was provided.\n")
        quit()

wordlist = get_wordlist_ql()
df = get_leadsfile_ql()

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
                print(index + "successful request")
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