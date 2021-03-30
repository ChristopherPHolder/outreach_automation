from docxtpl import DocxTemplate
import pandas as pd

def fill_temp(filename):
    df = pd.read_excel("leads/" + filename + '_clean' + ".xlsx") # Opens excel file into dataframe
    bosses = split_name(df)
    print(bosses)
    doc = DocxTemplate("word_templates/cold_postmail_1.docx")
    context = {
        'title' : "Herr",
        'last_name': 'Holder'
        }
    doc.render(context)
    doc.save("generated_doc.docx")
    return 0

def split_name(df):
    bosses = [] # Iniciates a list
    for i in df.index: 
        x = df['Geschäftsführer'][i].split()
        if x[0] == 'Herr' or x[0] == 'Frau':
            #print('title: ' + x[0])
            if x[1].endswith('.') == False:
                #print('last_name: ' + x[1])
                if x[len(x) - 1].endswith('.') == False:
                    bosses.append({
                        'id': i,
                        'title': x[0], 
                        'last_name': x[1], 
                        'first_name': x[len(x) - 1]
                        })
                    #print('first_name: ' + x[len(x) - 1])

            elif x[2].endswith('.') == False:
                #print('last_name: ' + x[2])
                if x[len(x) - 1].endswith('.') == False: 
                    #print('first_name: ' + x[len(x) - 1])
                    bosses.append({
                        'id': i,
                        'title': x[0], 
                        'last_name': x[2], 
                        'first_name': x[len(x) - 1]
                        })
    
    for boss in bosses: 
        print(boss)
    
    return bosses
