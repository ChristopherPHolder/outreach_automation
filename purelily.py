from scraper_leads_firmenacb import scrape_firmenabc
from scraper_url import add_url
from qualify_leads import qualify_leads_fn
from comp.get_user_input import get_leadsfile_ql, get_wordlist_ql, open_wordlist, open_excel
from temp_filler import extract_lead_data
from leads_cleaner import clean_leads


def operation_caller():
    # Printing general usage information for final user.
    print(" What operation would you like to run?\
        \nTo scrape leads from firmenabc type 'F' and return/enter\
        \nTo scrape additional URLSs for and existing file type 'U' and return/enter\
        \nTo qualify leads from an existing file type 'Q' and return/enter\
        \nTo scrape additional URLs and qualify the leads type 'UQ' and return/enter\
        \nTo complete all task as one operation leave the field emtry and return/enter\
        \nTo extract the information for mails and tempales type 'C' and return/enter\
        \nTo create outreach word files from the exel file 'W' and return/enter")
    operator = input("Operation: ")

    if operator == '':
        full_operation()

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

    else: 
        print("Invalid input, try running it again with the recomended inputs\n")

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
    df = clean_leads(filename)
    df.to_excel("leads/" + filename + '_clean' + ".xlsx")
    return df

def w_operation():
    data = open_excel()
    df = extract_lead_data(data)
    print(df)
    # Extract useful information
    # Introduce it into a template


operation_caller()