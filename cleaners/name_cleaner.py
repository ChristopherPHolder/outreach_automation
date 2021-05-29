import pandas as pd
from tqdm import tqdm
import gender_guesser.detector as gender
import re

def clean_names_in_file(filename):
    df = pd.read_excel("leads/%s.xlsx" % filename)
    df = clean_df_names(df)
    df.to_excel("leads/%s.xlsx" % filename, index=False)

def clean_df_names(df):
    for i in tqdm(df.index, desc='Cleaning names'):
        if pd.isnull(df['Geschäftsführer'][i]) == False:
            name = df['Geschäftsführer'][i]
            df.loc[i, 'Geschäftsführer'] = clean_name(name)
    return df

def clean_name(name):
    name = remove_urls_in_name(name)
    name = remove_junk_in_name(name)
    name = add_gender_title_to_name(name)
    return name

def remove_urls_in_name(name):
    name = remove_emails_in_name(name)
    name = remove_links_in_name(name)
    return name

def remove_emails_in_name(name):
    email_in_name = True
    while email_in_name:
        if '@' in name:
            name_s = name.split()
            for ns in name_s:
                if '@' in ns:
                    email = ns
            name = name.replace(email, '')
        elif '@' not in name:
            email_in_name = False
    return name

def remove_links_in_name(name):
    link_indicators = [
        'http', 'www.', '.com', '.de',
    ]
    for indicator in link_indicators:
        if indicator in name:
            name_s = name.split()
            for ns in name_s:
                if indicator in ns:
                    link = ns
                    name = name.replace(link, '')
    return name

def remove_junk_in_name(name):
    name = remove_junk_str_in_name(name)
    name = remove_junk_cap_str_at_end_of_name(name)
    name = remove_junk_space_in_name(name)
    return name

def remove_junk_str_in_name(name):
    junk_str_lst = [
        '\n', 'WP', '|', 'z. B.',
        'z.B.', '\ufeff',
        ]
    for j in junk_str_lst:
        name = name.replace(j, '')
    return name

def remove_junk_cap_str_at_end_of_name(name):
    name_s = split_double_name(name)
    for ns in name_s:
        for n in range(len(ns)):
            if n != 0:
                if ns[n].isupper():
                    name = name.replace(ns[n:], '')
    return name

def remove_junk_space_in_name(name):
    name = remove_double_space_in_name(name)
    name = remove_start_and_end_spaces_in_name(name)
    return name

def remove_double_space_in_name(name):
    double_spaces = True
    while double_spaces:
        if '  ' in name:
            name = name.replace('  ', ' ')
        elif '  ' not in name:
            double_spaces = False
    return name
    
def remove_start_and_end_spaces_in_name(name):
    name = remove_start_spaces_in_name(name)
    name = remove_end_spaces_in_name(name)
    return name

def remove_start_spaces_in_name(name):
    if name[0] == ' ':
        start_spaces = True
    else:
        start_spaces = False
    while start_spaces:
        if name[0] == ' ':
            name = name[1:]
        elif name[0] != ' ':
            start_spaces = False
    return name

def remove_end_spaces_in_name(name):
    if name[-1] == ' ':
        end_spaces = True
    elif name[-1] != ' ':
        end_spaces = False
    while end_spaces:
        if name[-1] == ' ':
            name = name[:-1]
        elif name[-1] != ' ':
            end_spaces = False
    return name

def add_gender_title_to_name(name):
    if 'Herr' not in name or 'Frau' not in name:
        gender_title_not_in_name = True
        name_s = split_double_name(name)
        d = gender.Detector(case_sensitive=False)
    elif 'Herr' in name or 'Frau' in name:
        gender_title_not_in_name = False
    while gender_title_not_in_name:    
        for ns in name_s:
            name_gender = d.get_gender(u"%s" % ns, u'germany')
            if name_gender == 'male'\
            or name_gender == 'mostly_male':
                return 'Herr' + ' ' + name
            elif name_gender == 'female'\
            or name_gender == 'mostly_female':
                return 'Frau' + ' ' + name
        gender_title_not_in_name = False
    return name

def split_double_name(name):
    name_s = re.split(' |-', name)
    return name_s