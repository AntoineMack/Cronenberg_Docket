"""Initial Search Program for hernia mesh docket. Looking to accomplish
4 functions.
    1.) Spell check medical terms,
    2.) User input keyword search (exact and like)
    3.) Artifact search and quantity, ie "*" for 2x
    4.) Range search of 2 words within x # of words

    """
import pandas as pd, numpy as np
import re
import csv

terms = []
ex_terms = []
af = {}
#set terms to search from user
def get_terms():
    more = "y"
    while more == 'y':
        new_term = input('insert term to search')
        terms.append(new_term)
        more = input('add another word? y or n')
        if more.lower() == 'y':
            more = 'y'
        elif more.lower() == "n":
            more = 'n'
        elif more.lower() != 'y' or 'n':
            print('entry not recognized')
            more = 'y'

# set exclusionary TermsList
def get_exclude_terms():
    more = "y"
    while more == 'y':
        new_term = input('insert terms to EXCLUDE from results')
        ex_terms.append(new_term)
        more = input('add another word? y or n')
        if more.lower() == 'y':
            more = 'y'
        elif more.lower() == "n":
            more = 'n'
        elif more.lower() != 'y' or 'n':
            print('entry not recognized')
            more = 'y'

def get_artifacts():
    more = "y"
    while more == 'y':
        new_art = input('insert artifact to search')
        occurances = input('how many occurences')
        af.update({new_art:occurances})
        more = input('add another artifact? y or n')
        if more.lower() == 'y':
            more = 'y'
            continue
        elif more.lower() == 'n':
            more = 'n'
        elif more.lower() != "y" or "n":
            print('entry not recognized')
            more = "y"


#set artifacts to search and how many from user

#set 2 term range & proximity
# class Proximity:
#     group1 = []
#     more = 'y'
#     while more == 'y'
#     fstword = input('insert 1st word')
#     sndword = input('insert 2nd word')
#     group1.extend((fstword,sndword))
#     prox = input('insert # of words apart')

#locate text column.  User must insure text is 3rd column
#load csv

user_excel = str(input('insert path of file'))
doc = pd.read_csv(user_excel + '.csv')

get_terms()
get_exclude_terms()

rel = str(doc.columns[2])  #relevant column name as a string
doc["Possible"] = pd.Series(dtype = str)  #possible columns
doc["Found"] = pd.Series(dtype = str) #posts terms found
regext = '[a-z]+'

for word in terms:  #Search for terms add indicator and words
    searched = word + regext
    for i in range(len(doc)):
        if re.findall(searched, doc[rel][i], re.IGNORECASE):
            doc.loc[i, "Possible"] = "X"
            if type(doc.loc[i, "Found"]) == float:
                doc["Found"][i] = []
                doc.loc[i, "Found"].append(word)
            elif type(doc.loc[i, "Found"]) == str:
                list(doc.loc[i, "Found"])
                doc.loc[i, "Found"].append(word)

for term in ex_terms: #Search for Excluded terms add indicator
    ex_searched = term + regext             #and terms
    for i in range(len(doc)):
        if re.findall(ex_searched, doc[rel][i], re.IGNORECASE):
            doc.loc[i, "Possible" ] = "O"
            if type(doc.loc[i, "Found"]) == float:
                doc["Found"][i] = []
                doc.loc[i, "Found"].append(term)
                #doc.loc[i, "Found"].append(term)
            elif type(doc.loc[i, "Found"]) == str:
                list(doc.loc[i, "Found"])
                doc.loc[i, "Found"].append(term)

#work flow will add an "X" if term exists then REMOVE
#the x on second pass if exclusionary term exists

#file to csv
save_name = str(input('Enter file name to save:'))
doc.to_csv(save_name + ".csv")
