from scraper_leads_firmenacb import scrape_firmenabc
from scraper_leads_gelbeseiten import scrape_gelbesieten

from scraper_url import add_url
from qualify_leads import qualify_leads_fn
from comp.get_user_input import get_leadsfile_ql, get_wordlist_ql, open_wordlist, open_excel, \
                                get_company_location, get_company_type
from leads_cleaner import clean_leads
from temp_filler import fill_temp 


def operation_caller():
    # Printing general usage information for final user.
    print(" What operation would you like to run?\
        \nTo scrape leads from GelbeSeiten type 'G' and return/enter\
        \nTo scrape leads from firmenabc type 'F' and return/enter\
        \nTo scrape additional URLSs for and existing file type 'U' and return/enter\
        \nTo qualify leads from an existing file type 'Q' and return/enter\
        \nTo scrape additional URLs and qualify the leads type 'UQ' and return/enter\
        \nTo complete all tasks mentioned as one operation leave the field emtry and return/enter\
        \nTo extract the information for mails and templates type 'C' and return/enter\
        \nTo create outreach word files from the exel file 'W' and return/enter\
        \nTo extract to extract informations for mails and the word files type 'CW' and return/enter\
        \nTo complete all tasks mentioned as one operation type 'X' and return/enter")
    operator = input("Operation: ")

    if operator == '':
        full_operation()

    elif operator == 'G' or operator == 'g':
        g_operation()

    elif operator == 'F' or operator == 'f':
        scrape_firmenabc()

    elif operator == 'U' or operator == 'u':
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
    print(df)

    # Exporting table in excel format
    filename = company_type + "_" + location
    df.to_excel("leads/" + filename + ".xlsx")

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