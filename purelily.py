from scraper_leads_firmenacb import scrape_firmenabc
from scraper_leads_gelbeseiten import scrape_gelbesieten

from scraper_url import add_url
from scraper_managing_director import add_managing_director
from qualify_leads import qualify_leads_fn
from comp.get_user_input import get_leadsfile_ql, open_wordlist,\
                                get_company_location, get_company_type,\
                                get_wordlist_locations

from cleaners.leads_cleaner import clean_leads
from cleaners.name_cleaner import clean_names_in_file
from temp_filler import fill_temp
from compile_leads import compile_leads

from tqdm import tqdm  # Progress bar / counter
import pandas as pd # Library to store and export data formated as a table

def operation_caller():
    # Printing general usage information for final user.
    print(
        " What operation would you like to run?\
        \nTo scrape leads from GelbeSeiten type 'G' and return/enter\
        \nTo scrape from all of Gemany from GelbeSeiten type 'GG' and return/enter\
        \nTo scrape managing directer from leads imprint type 'MD'and return/enter\
        \nTo compile leads type 'COMP' and return/enter\
        \nTo scrape leads from firmenabc type 'F' and return/enter\
        \nTo scrape additional URLSs for and existing file type 'U' and return/enter\
        \nTo qualify leads from an existing file type 'Q' and return/enter\
        \nTo scrape additional URLs and qualify the leads type 'UQ' and return/enter\
        \nTo complete all tasks mentioned as one operation leave the field emtry and return/enter\
        \nTo extract the information for mails and templates type 'C' and return/enter\
        \nTo create outreach word files from the exel file 'W' and return/enter\
        \nTo extract to extract informations for mails and the word files type 'CW' and return/enter\
        \nTo complete all tasks mentioned as one operation type 'X' and return/enter"
    )
    operator = input("Operation: ")

    if operator == '':
        full_operation()

    elif operator == 'G' or operator == 'g':
        g_operation()

    elif operator == 'GG' or operator == 'gg'\
        or operator == 'Gg' or operator == 'gG':
        gg_operation()

    elif operator == 'MD' or operator == 'md'\
        or operator == 'Md' or operator == 'mD':
        md_operation()
    
    elif operator == 'COMP' or operator == 'comp'\
        or operator == 'Comp':
        comp_operation()
    
    elif operator == 'CN' or operator == 'cn':
        cn_operation()

    elif operator == 'F' or operator == 'f':
        scrape_firmenabc()

    elif operator == 'U' or operator == 'u':
        # FIX ERROR RELATED TO MISSPLACEMENT OF DATA TODO
        # FUCK YOU PATRICK!!
        filename = get_leadsfile_ql()
        add_url(filename)
        
    elif operator == 'Q' or operator == 'q':
        q_operation()

    elif operator == 'UQ' or operator == 'uq':
        uq_operation()

    elif operator == 'C' or operator == 'c':
        c_operation()
    
    elif operator == 'W' or operator == 'w':
        w_operation()
    
    elif operator == 'CW' or operator == 'cw':
        cw_operation()

    elif operator == 'X' or operator == 'x':
        full_operation_x()

    else: 
        print("Invalid input, try running it again with the recomended inputs\n")

def g_operation():
    company_type = get_company_type()
    location = get_company_location()
    df = scrape_gelbesieten(company_type, location)
    # Exporting table in excel format
    filename = company_type + "_" + location
    df.to_excel("leads/" + filename + ".xlsx", index=False)

def gg_operation():
    company_type = get_company_type()
    locations_filename = get_wordlist_locations()
    location_list = open_wordlist(locations_filename)
    for location in tqdm(location_list['Cities'], desc='German-list'):
        df = scrape_gelbesieten(company_type, location)
        if df.empty:
            print('-->', location, 'failed')
            df_failed_cities = pd.read_excel("wordlist/failed_locations.xlsx")
            df_failed_cities = df_failed_cities.append({'Cities': location}, ignore_index=True)
            df_failed_cities.to_excel("wordlist/failed_locations.xlsx", index=False)
        else:
            filename = company_type + "_" + location
            df.to_excel("leads/germany/" + filename + ".xlsx", index=False)
            location_list = location_list.drop(index=(location_list[location_list['Cities'] == location].index))
            location_list.to_excel("wordlist/%s.xlsx" % locations_filename, index=False)

def md_operation():
    filename = input("Insert leads: ")
    df = add_managing_director(filename)
    df.to_excel('leads/' + filename + '.xlsx', index=False)

def comp_operation():
    print(
        'Make sure all leads you want to add are located in ../leads/compile/to_compile/.\
        \nand file you want to compile them to is the only file in ../leads/compile/compiled/.\
        \nAlso it will fail to compile leads with diferent format!\
        \nTo cancel the operation press cmd + c (Mac) or ctrl + c (Windows)')
    compile_leads()

def cn_operation():
    filename = input("Insert leads: ")
    clean_names_in_file(filename)

def full_operation():
    filename = scrape_firmenabc()
    filename = add_url(filename)
    wordlistfile = "wordlist"
    wordlist = open_wordlist(wordlistfile) 
    qualify_leads_fn(filename, wordlist)

def uq_operation():
    filename = get_leadsfile_ql()
    filename = add_url(filename)
    wordlistfile = "wordlist"
    wordlist = open_wordlist(wordlistfile) 
    qualify_leads_fn(filename, wordlist)

def q_operation():
    filename = get_leadsfile_ql()
    wordlistfile = "wordlist"
    wordlist = open_wordlist(wordlistfile) 
    qualify_leads_fn(filename, wordlist)

# Extracts information to only leave the information necesary for the postal mails and templates
def c_operation():
    filename = get_leadsfile_ql()
    filename = clean_leads(filename)
    return filename

def w_operation():
    filename = get_leadsfile_ql()
    fill_temp(filename)

def cw_operation():
    filename = c_operation()
    fill_temp(filename)

def full_operation_x():
    filename = scrape_firmenabc()
    filename = add_url(filename)
    wordlistfile = "wordlist"
    wordlist = open_wordlist(wordlistfile) 
    filename = qualify_leads_fn(filename, wordlist)
    filename = clean_leads(filename)
    fill_temp(filename)

operation_caller()