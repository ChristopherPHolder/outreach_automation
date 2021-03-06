import pandas as pd

# Important! this return file names they do not include paths! 
# Paths must be added afterwords depending on use

# Importing wordlist
def get_wordlist_ql():
    wordlistfile = input("Insert wordlist: ")
    if wordlistfile == "":
        print("The default wordlist used")
        wordlistfile = "wordlist.xlsx"
    try: 
        wordlist = pd.read_excel("wordlist/" + wordlistfile)
        print("Succesfully imported wordlist from: " + wordlistfile)
        return wordlist

    except FileNotFoundError:
        print("\nError: Wordlist file not found!")
        print("Check if you did any typos and that the file is in the correct folder.\
            \nOnce you found the error, try to run the program again.\
            \nRemeber you can leave the field blank and it will use wordlist.xlsx \n")
        quit()

# Import leads data
def get_leadsfile_ql():
    leadsfile = input("\nInsert leads: ")
    
    # Import generic file for testing
    if leadsfile == "t":
        print("The the testing leads file was used.")
        leadsfile = "steuerberater_kärnten_test.xlsx"
    try:
        df = pd.read_excel("leads/" + leadsfile)
        print("Succesfully imported leads from: " + leadsfile)
        return leadsfile

    except FileNotFoundError:
        print("\nError: leads file not found!\
            \n Check if you did any typos and that the file is in the correct folder\
            \nOnce you found the error, try to run the program again.")
        quit()

    except AssertionError:
        print("\nA leads file is necesarry for this program. No file name was provided.\n")
        quit()

    except IsADirectoryError:
        print("\nA leads file is necesarry for this program. No file name was provided.\n")
        quit()