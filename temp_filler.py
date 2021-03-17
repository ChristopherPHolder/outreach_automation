import pandas as pd

def extract_company_name(data):
    c_name = pd.DataFrame(data, columns= ['Firmenname'])
    return c_name

def extract_company_address(data):
    return 0

def extract_bosses_name(data):
    return 0

def extract_lead_data(data):
    c_name = extract_company_name(data)
    c_address = extract_company_address(data)
    c_boss = extract_bosses_name(data)
    return 0