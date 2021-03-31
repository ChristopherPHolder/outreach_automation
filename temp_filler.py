from docxtpl import DocxTemplate
import pandas as pd

def fill_temp(filename):
    df = pd.read_excel("leads/" + filename + ".xlsx") # Opens excel file into dataframe
    bosses = split_name(df) # Gets list of bosses and there information

    # Iterates over each boss and creates word file
    for boss in bosses: # Itereates over list of bosses
        doc = DocxTemplate("word_templates/cold_postmail_1.docx") # Open template
        doc.render(boss) # Introduces data into template 
        doc.save("pending_post/postmail_" + filename + "_" + str(boss['id']) + ".docx") # Creates new word file

    

# Creates a list of dicts with the information of the bosses
def split_name(df):
    bosses = [] # Iniciates an empty list
    prof_title = ['(FH)', 'Dipl.-', 'MBA', 'BSc']
    for i in df.index: # Loops over each row in the leads file
        print("Template index is: " + str(i))
        x = df['Geschäftsführer'][i].split() # Splits the bosses name into a list of strings
        if x[0] == 'Herr' or x[0] == 'Frau': # If the first word is a personal title
            if x[1].endswith('.') == False and x[1] not in prof_title: # If the does not end with a '.' (proficional titles en with a '.')
                print("Last name: " + x[1])
                if x[len(x) - 1].endswith('.') == False: # If last word does not end with '.' 
                    # Adds boss to list of bosses
                    bosses.append({
                        'id': i,
                        'title': x[0], 
                        'last_name': x[1], 
                        'first_name': x[len(x) - 1]
                        })

            elif x[2].endswith('.') == False and x[2] not in prof_title: # Since 2nd word ened in '.' check 3rd
                print("Last name: " + x[2])
                if x[len(x) - 1].endswith('.') == False: # Check if last word ends in '.'
                    # Adds boss to list of bosses
                    bosses.append({
                        'id': i,
                        'title': x[0], 
                        'last_name': x[2], 
                        'first_name': x[len(x) - 1]
                        })

            elif x[3].endswith('.') == False and x[3] not in prof_title: # Since 2nd word ened in '.' check 3rd
                print("Last name: " + x[3])
                if x[len(x) - 1].endswith('.') == False: # Check if last word ends in '.'
                    # Adds boss to list of bosses
                    bosses.append({
                        'id': i,
                        'title': x[0], 
                        'last_name': x[3], 
                        'first_name': x[len(x) - 1]
                        })

    for boss in bosses:
        print(boss['last_name'])
    return bosses
