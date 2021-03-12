from scraper_leads_firmenacb import scrape_firmenabc
from scraper_url import add_url
from qualify_leads import qualify_leads_fn
from comp.get_user_input import get_leadsfile_ql, get_wordlist_ql

def operation_caller():
    print(" What operation would you like to run?\
        \n To scrape leads from firmenabc type 'F' and return/enter\
        \n To scrape additional URLSs for and existing file type 'U' and return/enter\
        \n To qualify leads from an existing file type 'Q' and return/enter\
        \n To scrape additional URLs and qualify the leads type 'UQ' and return/enter\
        \n To complete all task as one operation leave the field emtry and return/enter")
    operator = input("Operation: ")

    if operator == '':
        full_operation()

    elif operator == 'F':
        scrape_firmenabc()

    elif operator == 'U':
        filename = get_leadsfile_ql()
        add_url(filename)
        
    elif operator == 'Q':
        filename = get_leadsfile_ql()
        wordlist = get_wordlist_ql()
        qualify_leads_fn(filename, wordlist)

    elif operator == 'UQ':
        filename = get_leadsfile_ql()
        filename = add_url(filename)
        qualify_leads_fn(filename, wordlist)

def full_operation():
    filename = scrape_firmenabc()
    filename = add_url(filename)
    wordlist = ""
    qualify_leads_fn(filename, wordlist)

operation_caller()