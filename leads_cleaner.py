import pandas as pd
def clean_leads(filename):
    df = pd.read_excel("leads/" + filename + ".xlsx") # Opens excel file
    df = find_boss(df) # Finds the boss and passes him to the correct column
    df = remove_extra_bosses(df) # Removes all unnecesary columns
    filename = filename + '_clean' # Update filename
    df.to_excel("leads/" + filename + ".xlsx") # Creates new Excel file
    
    return filename
    
def find_boss(df): 
    # Creates list of priorities
    priorities = [
        'Geschäftsführer', 
        'persönlich haftender Gesellschafter', 
        'Komplementär', 
        'Kommanditist'
        ]
    # Iterate over the leads from the excel file
    for i in df.index:
        print("Index iteration: " + str(i))
        # Check is lead doesnt have a clear boss
        if pd.isnull(df['Geschäftsführer - 1'][i]) == True:
            print("Geschäftsführer - 1 is emptry for " + df['Firmenname'][i])
            # Check if it has a boss any of the other fields
            loopbreaker = 0 # Incase lead has no boss at all create a infinate loop breaker.
            print("Memory safety: " + str(loopbreaker))
            while pd.isnull(df['Geschäftsführer - 1'][i]) == True and loopbreaker < 100: # Run until it finds a boss or 100 iterations
                loopbreaker += 1 # Safegard agains infinate loops
                print("Memory safety: " + str(loopbreaker))
                for z in priorities: # Goes over the priorities 
                    for x in range(1, 20): # Checks up to 18 priority termination numbers
                        try: 
                            boss = z + ' - ' + str(x) # Extracts boss name/title as in excel sheet
                            print("Checking for: " + boss)
                            if pd.isnull(df[boss][i]) == False: # Checks if cell is emprty or if boss is name is there
                                x = df[boss][i].split() # Split field into a list
                                print("Boss found as: " + boss)
                                if x[0] != 'Firma': # Check that first word is
                                    print(x[0])
                                    df['Geschäftsführer - 1'][i] = df[boss][i] # Adds the boss is name as boss 1
                        except KeyError: # In case boss title is out of range
                            break
    print("Fining boss process is completed")
    return df

def remove_extra_bosses(df):
    # Change the name of the column for the boss
    df = df.rename(columns={
        'Geschäftsführer - 1': 'Geschäftsführer', 
        'Tel_1': 'Tel', 
        'Mail_1': 'Mail'
        })

    # List of important labels/columns that will not be droped from the excel
    imp_info = [
        'Geschäftsführer', 
        'Bezirk/Ort/Plz', 
        'Firmenname', 
        'Straße',
        'PLZ', 
        'Stadt',
        'Tel', 
        'Mail', 
        'Web']

    # Drop all columns how's lable in not in imp_info (important_information)
    for i in df.columns:
        if i not in imp_info:
            df = df.drop(columns=i)

    for i in df.index:
        if pd.isnull(df['Geschäftsführer'][i]):
            print("Droping empty row: " + str(df.index[i]))
            print("Company dropped was: " + str(df['Firmenname'][i]))
            df = df.drop(df.index[i])

    return df
