from docxtpl import DocxTemplate
import pandas as pd

def fill_temp(filename):
    df = pd.read_excel("leads/" + filename + '_clean' + ".xlsx") # Opens excel file into dataframe
    bosses = split_name(df) # Gets list of bosses and there information

    # Iterates over each boss and creates word file
    for boss in bosses: # Itereates over list of bosses
        doc = DocxTemplate("word_templates/cold_postmail_1.docx") # Open template
        doc.render(boss) # Introduces data into template 
        doc.save("pending_post/postmail" + str(boss['id']) + ".docx") # Creates new word file

# Creates a list of dicts with the information of the bosses
def split_name(df):
    bosses = [] # Iniciates an empty list
    for i in df.index: # Loops over each row in the leads file
        x = df['Geschäftsführer'][i].split() # Splits the bosses name into a list of strings
        if x[0] == 'Herr' or x[0] == 'Frau': # If the first word is a personal title
            if x[1].endswith('.') == False: # If the does not end with a '.' (proficional titles en with a '.')
                if x[len(x) - 1].endswith('.') == False: # If last word does not end with '.' 
                    # Adds boss to list of bosses
                    bosses.append({
                        'id': i,
                        'title': x[0], 
                        'last_name': x[1], 
                        'first_name': x[len(x) - 1]
                        })

            elif x[2].endswith('.') == False: # Since 2nd word ened in '.' check 3rd
                if x[len(x) - 1].endswith('.') == False: # Check if last word ends in '.'
                    # Adds boss to list of bosses
                    bosses.append({
                        'id': i,
                        'title': x[0], 
                        'last_name': x[2], 
                        'first_name': x[len(x) - 1]
                        })
    return bosses
