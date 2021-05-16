import pandas as pd
import numpy as np

def add_managing_director(filename):
    df = pd.read_excel("leads/" + filename + ".xlsx")
    df = check_add_imprint_column(df)
    df = add_imprint(df)
    #print(df)
    return df

def add_imprint(df):
    n = 0
    for i in df.index:
        if pd.isnull(df['Geschäftsführer'][i]) == True\
        and pd.isnull(df['Web'][i]) == False:
            n += 1
            # check site for imprint
            print(n, i, df['Web'][i], df['Impressum'][i])
            

def check_add_imprint_column(df):
    print(list(df))
    if 'Impressum' not in list(df):
        df['Impressum'] = np.nan
    return df

def get_imprint_url():
    pass


                
                


# Open file as pd

# Add imprint urls
# Iterate over each lead
    # If lead does not have managing director
    # AND If has website AND no imprint
        # Open website
        # Def get_imprint_url
        # If has imprint
            # Add to pd

# def add manager names 
# Iterate over each lead
    # If lead does not have managing director
    # AND has imprint
        # Open imprint
        # If 'managing director' (list of words) in imprint
        # def try to parse data to extract names ':)
        # Add name to 'Maybe managing director'

# save file
# close file

# Def get imprint
# Def get mananger name