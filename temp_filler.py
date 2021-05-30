from docxtpl import DocxTemplate
import pandas as pd
from tqdm import tqdm

def fill_temp(filename, name_order='tfl'):
    df = pd.read_excel("leads/%s.xlsx" % filename)
    bosses = get_bosses_name(df, name_order)

    for boss in tqdm(bosses, desc='Filling templates'):
        doc = DocxTemplate("word_templates/cold_postmail_2.docx")
        doc.render(boss)
        id = str(boss['id'])
        doc.save("pending_post/postmail_%s_%s.docx" % (filename, id))

def get_bosses_name(df, name_order):
    bosses = []
    prof_titles = get_prof_titles()

    for i in tqdm(df.index, desc='Processing names'):
        x = df['Geschäftsführer'][i].split()
        if x[0] == 'Herr' or x[0] == 'Frau':
            name_struct = get_name_struct(x, prof_titles)
            boss = get_boss_info(i, x, name_order, name_struct)
            if boss != None:
                bosses.append(boss)
    return bosses

def get_name_struct(x, prof_titles):
    if (x[1].endswith('.') == False and
    x[1] not in prof_titles and
    x[len(x) - 1].endswith('.') == False):
        return 'Gender_Name_Name'
    elif (x[2].endswith('.') == False and
    x[2] not in prof_titles and
    x[len(x) - 1].endswith('.') == False):
        return 'Gender_NotName_Name_Name'
    elif (x[3].endswith('.') == False and
    x[3] not in prof_titles and
    x[len(x) - 1].endswith('.') == False):
        return 'Gender_NotName_NotName_Name_Name'


def get_boss_info(i, x, name_order, name_struct):
    boss = {'id': i, 'title': x[0]}
    if name_struct == 'Gender_Name_Name':
        return get_boss_with_struct_gnn(boss, x, name_order)
    elif name_struct == 'Gender_NotName_Name_Name':
        return get_boss_with_struct_gxnn(boss, x, name_order)
    elif name_struct == 'Gender_NotName_NotName_Name_Name':
        return get_boss_with_struct_gxxnn(boss, x, name_order)

def get_boss_with_struct_gnn(boss, x, name_order):
    if name_order == 'tlf':
        boss['last_name'] = x[1].replace(',', '')
        boss['first_name'] = x[len(x) - 1]
    elif name_order == 'tfl':
        boss['last_name'] = x[len(x) - 1]
        boss['first_name'] = x[1].replace(',', '')
    return boss

def get_boss_with_struct_gxnn(boss, x, name_order):
    if name_order == 'tlf':
        boss['last_name'] = x[2].replace(',', '') 
        boss['first_name'] = x[len(x) - 1]
    elif name_order == 'tfl':
        boss['last_name'] = x[len(x) - 1]
        boss['first_name']= x[2].replace(',', '')
    return boss


def get_boss_with_struct_gxxnn(boss, x, name_order):
    if name_order == 'tlf':
        boss['last_name'] = x[3], 
        boss['first_name'] = x[len(x) - 1]
    elif name_order == 'tfl':
        boss['last_name'] = x[len(x) - 1]
        boss['first_name'] = x[3]
    return boss

def get_prof_titles():
    prof_titles = [
        '(FH)', 'Dipl.-', 'MBA', 
        'BSc', 'Dr.',
    ]
    return prof_titles