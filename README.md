# PureMind_automation
Automating the processes in PureMind Digital Gmbh

Eventually this Repo will automate all possible aspects and processes conducted by PureMind Digital

#### INSTRUCTIONS FOR USE ####
Start by installing the dependencies with pipenv. 
Make sure you have Pipenv Installed

  $ pip install Pipenv

Then install and activate the requirements located in Piplock

  $ pipenv install Piplock

Then activate the shell
  
  $ pipenv shell

Then download the nlp model

  $ python -m spacy download de_core_news_md

Them run the program

  $ python purelily.py

Them provide the input which is prometed from the terminal. 

#### REPO CONTENT #### 
Currently there are 3 independent processes automated on this CLI application

## scraper_leads_firmenabc.py 
  As the name implies it scrapes leads information from the website firmenabc.at

## scraper_url.py 
  Which takes a file with the same structure as the one produced by scraper_leads_firmenabc.py and attempts to find the website of the ones that are missing.
  
## qualifier_leads.py
  IT qualifies the leads ranking them with the main criteria how badly are they looking for employes.
  
In addition to that there is an application which cordinates the activites allowing them to flow as one process

## purelily.py
  It will run all the aplications in a sequence.
  This programed is named after the person all these softwares where modeled after. 