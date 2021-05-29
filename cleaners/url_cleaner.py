import pandas as pd
from tqdm import tqdm

def clean_urls_in_file(filename):
    df = pd.read_excel("leads/%s.xlsx" % filename)
    df = clean_df_urls(df)
    df.to_excel("leads/%s.xlsx" % filename, index=False)

def clean_df_urls(df):
    for i in tqdm(df.index, desc='Cleaning URLs'):
        if pd.isnull(df['Web'][i]) == False:
            url = df['Web'][i]
            df.loc[i, 'Web'] = clean_url(url)
    return df

def clean_url(url):
    url = remove_url_protocol(url)
    url = remove_url_www_subdomain(url)
    url = remove_url_path(url)
    return url


def remove_url_protocol(url):
    url = url.replace('https://', '')
    url = url.replace('http://', '')
    return url

def remove_url_www_subdomain(url):
    url = url.replace('www.', '')
    return url

def remove_url_path(url):
    url_s = url.split('/')
    try: 
        url = url_s[0]
    except KeyError:
        pass
    return url
