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

########### set artifacts to search and how many from user###############
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

############### set 2 term range & proximity###########################

#currently only has functionality for 1 proximity search
def Get_Prox_Words():
    group1 = []
    more = "y"
    while more == "y":
        fstword = input('insert 1st word')
        sndword = input('insert 2nd word')
        group1.extend((fstword,sndword))
        prox = input('insert # of words apart')
        ans = input('Is this this correct \
                1st word is ' + str(fstword) +'\
                2nd word is ' + str(sndword) +'\
                proximity is ' + str(prox) )
        if ans == "y":
            more = "n"
            pass
        elif ans == "n":
            ans = "n"
            continue
        elif ans != "y" or "n":
            print('entry not recognized')
            continue
    Get_Prox_Words.prox = prox
    Get_Prox_Words.fstword = fstword
    Get_Prox_Words.sndword = sndword

######### creates list of word indexes ####################################
# splits a long string into a list of strings then iterates through, "i" will

def Find_Index():
    index_list = []
    for i in range(len(mesh_test.split())):
        if re.search('infect' + regext, mesh_test.split()[i]):
            index_list.append(i)
        else:
            pass
    return index_list


########creates range objects from indexes to grab sub strings ngrams away#####
#listofin is from Find_Index
#ranges is from prox of Get_Prox_Words
def Range_Maker(listofin, ranges):
    range_list = []
    for i in listofin:
        begin = i - (ranges)
        end = i + (ranges + 1)
        range_add = range(begin, end)
        range_list.append(range_add)
    return range_list

########### Takes range object and creates sub strings from relevant list######
#rel_list is long string that is being ex_searched
# range_object is from Range_Maker
def Grab_Sub_Strings(rel_list, range_object):
    new_strings = []
    for i in range_object: #Ranger holds 2 range objects for search window
        window = "" # window in compile string in range
        for k in i:
            window += (rel_list.split()[k] + " ")
        new_strings.append(window)
    return new_strings

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
