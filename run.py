from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from tqdm import tqdm
import pandas as pd
import time


def scrape_firmenabc():

    companytype = "steuerberater"
    location = ''
    limit = 100
    limit_set = 0

    options = Options()
    options.headless = False

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://www.firmenabc.at/")

    # Wait for cookie popup to load
    while True:
        try:
            # Accept cookie popup
            cookiesHandle = driver.find_element_by_xpath(
                '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'
            )
            cookiesHandle.click()
            break
        except:
            # Wait a sec to see if its there now
            time.sleep(1)

    # Input user input into search
    searchInput1 = driver.find_element_by_xpath('//*[@id="what"]')
    searchInput1.send_keys(companytype)

    searchInput2 = driver.find_element_by_xpath('//*[@id="where"]')
    searchInput2.send_keys(location)

    sendInput = driver.find_element_by_xpath('//*[@id="btnSearch"]')
    sendInput.click()

    listOfLinks = []
    condition = True

    m = 0

    print("Obtaining links...")
    while condition:
        CompanyList = driver.find_elements_by_xpath('//a[@itemprop="url"]')
        s = 0
        for el in CompanyList:
            listOfLinks.append(el.get_property("href"))
            s += 1
        try:
            if driver.find_element_by_class_name("next").get_property("href") != "":
                driver.find_element_by_class_name("next").click()
            else:
                condition = False
        except:
            condition = False

        m += 1

    alldetails = []


    print("Extracting data...")
    for i in tqdm(listOfLinks):
        # print("iterating")
        driver.get(i)
        temp = {}
        temp["Firma/Suchbegriff"] = companytype
        temp["Bezirk/Ort/Plz"] = location
        try:
            name = driver.find_element_by_xpath('//div[@itemprop="name"]').text
            temp["Firmenname"] = name
        except:
            temp["Firmenname"] = ""
            # print('error en name')
        try:
            streetAdress = driver.find_element_by_xpath(
                '//span[@itemprop="streetAddress"]'
            ).text
            temp["Straße"] = streetAdress
        except:
            temp["Straße"] = ""
            # print('error in streeAddress')
        try:
            postalCode = driver.find_element_by_xpath('//span[@itemprop="postalCode"]').text
            temp["PLZ"] = postalCode
        except:
            temp["PLZ"] = ""
            # print('error in postalcode')
        try:
            addressLocality = driver.find_element_by_xpath(
                '//span[@itemprop="addressLocality"]'
            ).text
            temp["Stadt"] = addressLocality
        except:
            temp["Stadt"] = ""
            # print('error in addressLocality')
        try:
            telephones = driver.find_elements_by_xpath('//span[@itemprop="telephone"]')
            texts = [i.text for i in telephones]
            try:
                temp["Tel_1"] = texts[0]
            except:
                temp["Tel_1"] = ""
            try:
                temp["Tel_2"] = texts[1]
            except:
                temp["Tel_2"] = ""
        except:
            temp["Tel_1"] = ""
            temp["Tel_2"] = ""
        try:
            faxNumber = driver.find_element_by_xpath('//span[@itemprop="faxNumber"]').text
            temp["Fax"] = faxNumber
        except:
            temp["Fax"] = ""
            # print('error in faxnomber')
        try:
            email = driver.find_element_by_xpath(
                '//*[@id="main-container"]/div/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/a'
            ).text
            temp["Mail - 1"] = email
        except:
            temp["Mail - 1"] = ""
            # print('error en email')
        try:
            web = driver.find_element_by_xpath('//a[@itemprop="url"]').text
            temp["Web"] = web
        except:
            temp["Web"] = ""
            # print('error en web')

        ##### CREDIT INFO ####
        # Descripcion del puesto
        try:
            descripcionPuesto = driver.find_element_by_xpath(
                '//span[@itemprop="description"]'
            ).text
            temp["Tätigkeitsbeschreibung - 1"] = descripcionPuesto
        except:
            temp["Tätigkeitsbeschreibung - 1"] = ""
            # print("error en descripcionPuesto")

        # Numero UUUD
        try:
            numeroUID = driver.find_element_by_xpath('//span[@itemprop="vatID"]').text
            temp["UID-Nummer:"] = numeroUID
        except:
            temp["UID-Nummer:"] = ""
            # print("error en numeroUID")

        # Fecha de inicio de forma juridica
        try:
            fechaInicioFormaJuridica = driver.find_element_by_xpath(
                '//span[@itemprop="foundingDate"]'
            ).text
            temp["Beginndatum der Rechtsform:"] = fechaInicioFormaJuridica
        except:
            temp["Beginndatum der Rechtsform:"] = ""
        try:
            i = 0
            condition = True
            while condition:
                accionistas = driver.find_elements_by_xpath(
                    '//*[@id="crefo"]/div[2]/div[{0}]'.format(5 - i)
                )
                list_of_strings = []
                for a in accionistas:
                    b = a.text
                    if b == "" and b.isspace():
                        print(".")
                    else:
                        list_of_strings.append(b)
                list_of_strings = list_of_strings[0].split("\n\n")

                if "Handelnde Personen:" in list_of_strings:
                    list_acc = []
                    prove = []
                    for item in list_of_strings[1:]:
                        dictjsn = {}
                        accionistas = item.split("\n")
                        if len(accionistas) > 1:
                            prove.append(accionistas[0])
                            n = prove.count(accionistas[0])
                            temp[accionistas[0] + " - " + str(n)] = accionistas[1]
                            if "Anteil" in accionistas[3]:
                                temp["Anteil" + " - " + str(n)] = accionistas[3][7:]
                            list_acc.append(dictjsn)

                        if len(accionistas) == 1:
                            temp[accionistas[0] + " - " + str(1)] = accionistas[1:]

                    condition = False
                i += 1
        except:
            continue

        alldetails.append(temp)
        
        # Code to exit after passing a limit %
        limit_set += 1
        if limit_set == int(len(listOfLinks) * limit / 100):
            break

    # Converting to table format
    df = pd.DataFrame(alldetails)
    print(df)  # Visualizacion
    
    # Exporting table in excel format
    filename = companytype + "_" + location
    df.to_excel("leads/" + filename + ".xlsx", index=False)

    driver.close()

    return filename