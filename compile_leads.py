import pandas as pd
import numpy as np
import os

def compile_leads():
    df_comp = get_compiled_leads()
    leads_filename_list = get_list_leads_to_compile()
    for filename in leads_filename_list:
        df_to_comp = get_leads_to_compile(filename)
        df_comp = insert_new_leads(df_comp, df_to_comp)
        df_comp = df_comp.drop_duplicates()
    save_compiled_leads(df_comp)
    print(df_comp)

def get_compiled_leads():
    files = os.listdir('leads/compile/compiled/')
    for file in files:
        if file.endswith('.xlsx'):
            filename = file
            return pd.read_excel("leads/compile/compiled/%s" % filename)

def save_compiled_leads(df_comp):
    files = os.listdir('leads/compile/compiled/')
    for file in files:
        if file.endswith('.xlsx'):
            filename = file
            df_comp.to_excel("leads/compile/compiled/%s" % filename, index=False)

def get_list_leads_to_compile():
    files = os.listdir('leads/compile/to_compile/')
    leads_filename_list = []
    for file in files:
        if file.endswith('.xlsx'):
            leads_filename_list.append(file)
    return leads_filename_list
    
def get_leads_to_compile(filename):
    return pd.read_excel("leads/compile/to_compile/%s" % filename)

def insert_new_leads(df_comp, df_to_comp):
    df_comp = insert_new_columns(df_comp, df_to_comp)
    df_comp = insert_new_leads_info(df_comp, df_to_comp)
    return df_comp

def insert_new_columns(df_comp, df_to_comp):
    columns_to_comp = list(df_to_comp.columns)
    columns_comp = list(df_comp.columns)
    for column_to_comp in columns_to_comp:
        if column_to_comp not in columns_comp:
            df_comp[column_to_comp] = np.nan
    return df_comp

def insert_new_leads_info(df_comp, df_to_comp):
    return df_comp.append(df_to_comp)
