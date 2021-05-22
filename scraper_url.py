import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlparse
import re
import pandas as pd
from tqdm import tqdm

def add_url(filename):
    # Importing data with urls
    df = pd.read_excel("leads/" + filename + ".xlsx")
    # Filtering companies with web
    try:
        df.drop("Unnamed: 0", axis=1, inplace=True)
    except:
        pass

    df_no_web = df[pd.isnull(df["Web"])].reset_index(drop=True)
    df_web = df[pd.notnull(df["Web"])].reset_index(drop=True)

    def google_search(query):
        g_clean = []  # Inicializing the list where search results are stored
        url = "https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8".format(
            query
        )
        # This is the actual query we are going to scrape
        try:
            html = requests.get(url)
            if html.status_code == 200:
                soup = BeautifulSoup(html.text, "lxml")
                a = soup.find_all("a")  # a is a list
                for i in a:
                    k = i.get("href")
                    try:
                        try:
                            m = re.search("(?P<url>https?://[^\s]+)", k)
                        except:
                            m = re.search("(?P<url>http?://[^\s]+)", k)
                        n = m.group(0)
                        rul = n.split("&")[0]
                        domain = urlparse(rul)
                        if re.search("google.com", domain.netloc):
                            continue
                        else:
                            g_clean.append(rul)
                    except:
                        continue
        except Exception as ex:
            print(str(ex))
        finally:
            return g_clean

    match_by_company_name = []
    list_of_company_names = df_no_web.Firmenname.astype(str).tolist()

    for company_name in tqdm(list_of_company_names):
        list_of_links = google_search(company_name)
        match_by_link = []
        
        for link in list_of_links:
            key_words = company_name.lower().split(" ")
            m = re.search("^(?:[^\/]*\/){2}[^\/]+", link)
            n = m.group(0)

            # key_words = company_name.lower().split(' ')
            matches = sum([word in n for word in key_words])
            if matches >= 1:
                match_by_link.append(link)
        try:
            match_by_company_name.append(match_by_link[0])  # only paste the first
        except:
            match_by_company_name.append("")

    df_no_web.insert(loc=0, column="URL", value=match_by_company_name)
    df_web.insert(loc=0, column="URL", value="")

    df_t = df_web.append(df_no_web, ignore_index=True, sort=False)

    n = df_t.shape[0]
    for i in range(n):
        if df_t.loc[i, "URL"] != "":
            df_t.loc[i, "Web"] = df_t.loc[i, "URL"]

    df_t.drop("URL", axis=1, inplace=True)

    filename = filename + "_plus"
    df_t.to_excel("leads/" + filename + ".xlsx", index=False)

    return filename
