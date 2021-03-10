from scraper_leads_firmenacb import scrape_firmenabc
from scraper_url import add_url
from qualify_leads import qualify_leads_fn

def scrape_leads():
    filename = scrape_firmenabc()
    filename = add_url(filename)
    wordlist = ""
    filename = qualify_leads_fn(filename, wordlist)

    return filename

scrape_leads()